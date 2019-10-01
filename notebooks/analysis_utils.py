from statsmodels.api import OLS, Logit
from statsmodels.tools.tools import add_constant
from scipy.stats import zscore

def topic_regression(df,target_list,exog,controls,model,binarise=False,standardise=True,cov='HC1'):
    '''
    
    This function regresses topic weights (or their binarisation) on predictors.
    
    Arguments:
        -Df with the variables
        -target_list: target variables. This is a list we loop over. 
        -exog: exogenous variable
        -controls
        -model type. OLS? Logit? TODO fix the logit
        -Binarise in case we are using logit. If not False, the value is the threshold 
            TODO when we binarise the highly detailed models, some of them become all zeros. This will work better
            with the mopre aggregate topics
        -Standardise if we standardise and log the topic weights
    
    Returns
        -A list of statsmodels summaries

    
    '''
    
    #Drop rows with missing values - sm doesn't like them
    df_2 = df[target_list+exog+controls].dropna(axis=0)
    
    #Standardise targets?
    if standardise==True:
        df_2[target_list] = (np.log(df_2[target_list]+0.00000001)).apply(zscore).astype(float)
    
    #Binarise targets if we are doing a logit
    if binarise!=False:
        df_2[target_list] = df_2[target_list].applymap(lambda x: x>binarise).astype(float)
    
    
    #Extract the exogenous and controls, add constant and cast as float
    exog_controls = add_constant(df_2[exog+controls]).astype(float)
    

    #Container output
    out = []
    coeffs = []
    
    #One regression for each target
    for t in list(target_list):
        
        #There we gp. 
        reg = model(endog=df_2[t],exog=exog_controls).fit(cov_type=cov,disp=0)
        
        out.append(reg.summary())
        
        #coeffs.append(reg)
        if model == OLS:
            coeffs.append(pd.Series([float(reg.params[exog]),float(reg.pvalues[exog]),float(reg.rsquared)],name=t))
            reg_coeff = pd.concat(coeffs,axis=1).T
            reg_coeff.columns = ['coefficient','p_value','r_square']
    
        else:
            coeffs.append(pd.Series([float(reg.params[exog]),float(reg.pvalues[exog]),float(reg.prsquared)],name=t))
            reg_coeff = pd.concat(coeffs,axis=1).T
            reg_coeff.columns = ['coefficient','p_value','pr_square']
 
    
    return([out,reg_coeff.sort_values('coefficient',ascending=False)])
        
        
def topic_comparison(df,target_list,exog,concept_lookup,quantiles=np.arange(0,1.1,0.2),thres=0):
    '''
    This function compares the distribution of activity in various topics depending on an exogenous variable of interest. 
    
    Args:
        Df with the topic mix and metadata
        target_list are the topics to consider
        exog is the variable to crosstab topics against
        concept_lookup is a df with the median proximity of each topic to the concepts
        quantiles is how we discretise the concept lookup (default value is quintiles)
        thres: =limit for considering a topic as present

    
    '''
    
    #Copy df
    
    df_2 = df.copy()
    
    #Discretise the concept lookup
    
    conc_discr = concept_lookup.apply(lambda x: pd.qcut(x,q=quantiles,labels=False,duplicates='drop'))

    
    #Calculate levels of activity per topic based on the exog variable
    
    topic_distr = pd.concat([pd.crosstab(df_2[exog],df_2[t]>thres)[True] for t in target_list],axis=1).T
    topic_distr.index = target_list
    
    
    #Merge the count with the concept lookup
    disc = pd.melt(pd.concat([topic_distr,conc_discr],axis=1).reset_index(drop=False),id_vars=['index']+list(conc_discr.columns))
    
    #This is the list where we store the results
    store={}
    
    for c in concept_lookup.columns:
        
        out = pd.pivot_table(disc.groupby([c,'variable'])['value'].sum().reset_index(drop=False),index=c,columns='variable',values='value')
        #out.apply(lambda x: x/x.sum()).plot.bar()
        
        store[c] = out
                                      
    #Output dfs with the comparisons
    return(store)


def make_exog(df,value_container,value,make_dummy=True):
    '''
    This creates exogenous variables for modelling later.
    
    Argument:
        -df contains the variable where we want to find a value
        -variable_container is the column where we want to look for the value
        -value is the value we are looking for
        -make_dummy: if true it just counts if the value is present. If false, it counts how many times it happens. 
        
    Output
        -A df with the new column (named)
    
    
    '''
    
    df_2 = df.copy()
    
    #Create a tidy variable name
    column_name = re.sub(' ','_',value.lower())
    
    #If we want to create a dummy...
    if make_dummy == True:
        
        #We just look for it in the value container
        #There are some missing values so we have some control flow to manage that. 
        df_2[column_name] = [value in x if type(x)==list else np.nan for x in df_2[value_container]]
    
    else:
        
        #Otherwise, we count how many times it occurs
        #We deal with missing values ('non lists') as before
        df_2[column_name] = [x.count(value) if type(x)==list else np.nan for x in df_2[value_container]]
        
    return(df_2)
    

def make_trend_plot(df,topics_to_consider,top_n,ax,top_year=2018,thres=0.05,period=[2005,2019],alpha=0.3):
    '''
    Generates a similar plot to those above but with automatic identification of the top trends
    
    Args:
        Df is the topic mix (we will often have subsetted this to focus on a particular type of organisation)
        top_n is the top number of entities to label and display
        threshold for considering that a topic is present in a paper
        period is a list with the period we are considering
        
    Returns a similar plot to above but visualising the top n trends 

    
    '''
    
    #Check for topics with no activity:
    total_presence = (df[topics_to_consider]>thres).sum()
    no_values = total_presence.index[total_presence==0]
    
    topics_to_consider = [x for x in topics_to_consider if x not in no_values]
    
    
    #Calculate topic trends
    topic_trends = trend_analysis(df,topics_to_consider,thres=thres,year_lim=period)
    
    #Calculate all papers, for normalisation
    all_years = df['year'].value_counts()
    
    #Normalise
    topic_trends_norm = topic_trends.apply(lambda x: x/all_years).dropna()
    
    top_topics = topic_trends_norm.T.sort_values(top_year,ascending=False).index[:top_n]
    
    
    make_highlight_plot(topic_trends_norm,top_topics,cmap='Dark2',ax=ax,alpha=alpha)
    
    
    
def quick_plot(df,var_subset,topics_to_consider=topics_filtered,n_tops=8):
    '''
    Creates trend plots based on different categories.
    
    Args:
        df with papers and topics
        var_subset is the variable we want to consider (will generally be a boolean)
        n_tops: number of top institutions to visualise
    
    '''
    
    fig,ax = plt.subplots(figsize=(10,8))

    my_df = df.loc[df[var_subset]==True]
    
    make_trend_plot(my_df,topics_filtered,n_tops,ax=ax,top_year=2018,alpha=0.2)
    
    ax.set_title(var_subset)
    