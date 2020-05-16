#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 12:11:05 2019

@author: dairongyi
"""
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


# Get ready for MAF dataframe
maf_file = "TCGA.BRCA.varscan.6c93f518-1956-4435-9806-37185266d248.DR-10.0.somatic.maf.gz"
maf_df = pd.read_csv(maf_file, 
                     sep="\t", 
                     comment="#", 
                     usecols=["Hugo_Symbol", "Variant_Classification", "Tumor_Sample_Barcode",  "PolyPhen"])
maf_df = maf_df[maf_df["Variant_Classification"] != "Silent"]  

# Get ready for clinical dataframe
clinical_file = "clinical.tsv"
clinical_df = pd.read_csv(clinical_file, sep="\t")
clinical_df = clinical_df[(clinical_df["project_id"]=="TCGA-BRCA") & (clinical_df["days_to_death"] != "--")]
clinical_df.index = clinical_df["submitter_id"]

# Mutation counts
maf_df["Count"] = 1
tumor_sample_df = pd.pivot_table(maf_df, values="Count", index="Tumor_Sample_Barcode", columns="Hugo_Symbol", aggfunc=np.sum)
tumor_sample_df = tumor_sample_df.replace(np.nan, 0)
#tumor_sample_df = tumor_sample_df.loc[:, tumor_sample_df.sum()>=10]
tumor_sample_df.index = [i[0:12] for i in tumor_sample_df.index]
tumor_sample_df_new = pd.concat([tumor_sample_df, clinical_df["days_to_death"]], axis = 1, join="inner")
y_count = tumor_sample_df_new.iloc[0:-1,].sum(axis=1).to_numpy()
mean = (np.mean(y_count))
std=np.std(y_count)
print(mean, std)
# Polyphen score
maf_df["PolyPhen_Num"] = maf_df["PolyPhen"].str.extract('(\d*\.\d+|\d+)', expand=False).astype(float).replace(np.nan, 0)
polyphen_df = pd.pivot_table(maf_df, values="PolyPhen_Num", index="Tumor_Sample_Barcode", columns="Hugo_Symbol", aggfunc=np.sum)
polyphen_df = polyphen_df.replace(np.nan, 0)
polyphen_df.index = [i[0:12] for i in polyphen_df.index]
polyphen_df = polyphen_df[tumor_sample_df.columns]
polyphen_df_new = pd.concat([polyphen_df, clinical_df["days_to_death"]], axis = 1, join = "inner")
print(polyphen_df_new.columns[984])
y_poly = polyphen_df_new.iloc[0:-1,].sum(axis=1).to_numpy()
print(np.mean(y_poly))
# pca = PCA(0.85)
# principal_components = pca.fit_transform(tumor_sample_df)
# principal_df = pd.DataFrame(data = principal_components, index = tumor_sample_df.index)
# #principal_df[principal_df<0] = 0
# principal_df_new = pd.concat([principal_df, clinical_df["days_to_death"]], axis = 1, join = "inner")

# Run linear regression
def linear_regression(x, y, cv, slope_i=None):
#    x_train, x_test, y_train, y_test = train_test_split(x_2, y_2, test_size=0
    model = LinearRegression().fit(x, y)
    score = cross_val_score(model, x, y, cv=cv)
    y_predict = cross_val_predict(model, x, y, cv=cv, method="predict")
    r_sq = model.score(x, y)
    slope = model.coef_
#    try: 
#        slope_df = pd.DataFrame(slope, index=slope_i)
#    except:
#        pass
    print("cross_val_score is: ", np.mean(score))
#    print(y_predict)
    print('coefficient of determination:', r_sq)
    print('intercept:', model.intercept_)
    print('slope:', slope)
    return [slope, y_predict]

def lasso_regression(x, y, cv):
#    model = Lasso(alpha=20).fit(x,y)
    lasso = Lasso().fit(x, y)
    
    params = {'alpha': [0.1, 1, 10, 100]}
    lasso_regressor = GridSearchCV(lasso, params, scoring='r2' )
    result = lasso_regressor.fit(x, y)
#    
##    slope = result.coef_
    print('Best Score: ', result.best_score_)
    print('Best Params: ', result.best_params_)
#    print('coefficient of determination: '+ slope)
    
    score = cross_val_score(result, x, y, cv=cv)
    y_predict = cross_val_predict(result, x, y, cv=cv, method="predict")
    r_sq = result.score(x, y)
    slope = result.coef_
    
    print("cross_val_score is: ", np.mean(score))
#    print(y_predict)
    print('coefficient of determination:', r_sq)
#    print('intercept:', model.intercept_)
    print('slope:', slope)
    return [slope, y_predict, score]
#
if __name__ == "__main__":    
#    x_1 = principal_df_new.iloc[:, 0:-1].to_numpy()
#    y_1 = principal_df_new.iloc[:, -1].astype(float).to_numpy()
##    slope_i = tumor_sample_df.columns
#    result = linear_regression(x=x_1, y=y_1, cv=5)
##    print(result[1])
#   
    print("---------------Polyphen------------------")
    
    x_2 = polyphen_df_new.iloc[:, 0:-1].to_numpy()
    y_2 = polyphen_df_new.iloc[:, -1].astype(float).to_numpy()
#    x_train, x_test, y_train, y_test = train_test_split(x_2, y_2, test_size=0.3)
#    slope_i = polyphen_df.columns
    result1 = linear_regression(x=x_2, y=y_2, cv=5)
    print("---------------Lasso---------------")
    result2 = lasso_regression(x = x_2, y = y_2, cv = 5)

    