#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import xarray as xr
from datetime import datetime, timedelta


def get_avg_predictor(pred_fields, DWT_bmus):
    # get an average predictor (SLP or SST) field for each month and each DWT in the historical period
    
    #first get them to have the same times
    DWT_bmus = DWT_bmus.swap_dims({'n_components':'time'}) 
    hist_fields = DWT_bmus.merge(pred_fields,join = 'inner')
    
    mean_DWT_pred ={}

    for d in range(1,43):
        hist_fields_bmu = hist_fields.sel(time = hist_fields['sorted_bmus_storms'] == d)
        mean_DWT_pred[d] = np.nanmean(hist_fields_bmu['pred_fields'],0)


    mean_month_pred ={}
    
    grid_len = len(mean_DWT_pred[1])
    for m in range(1,13):
        hist_fields_month = hist_fields.sel(time = hist_fields['time.month']== m)
        stacked_pred=np.empty((0,grid_len),dtype=object)

        for d in range(1,43):
            dwt_pred = hist_fields_month.sel(time = hist_fields_month['sorted_bmus_storms']==d)
            num_times_DWT = int(dwt_pred['sorted_bmus_storms'].count())            
            stacked_pred = np.append(stacked_pred,np.tile(mean_DWT_pred[d],(num_times_DWT,1)),axis=0)
        
        mean_month_pred[m] = np.nanmean(stacked_pred,0) # find the mean of the month
    
    return mean_month_pred, mean_DWT_pred




def monthly_pred_from_DWT(mean_DWT_pred,mean_month_pred, DWT_bmus, mode = 'hist'):
    '''
    predictor_fields
    mode = 'hist' or 'sim'  - input variables have different naming conventions
                               and sim must be run for x # of DWT sims
    returns a timeseries of monthly predictor (SLP), filling in the average SLP for each DWT
    and then averaging over the month and subtracting by the monthly average 
    
    '''
    
    if mode == 'hist':
        print('working on hist period')
        DWT_bmus = DWT_bmus.swap_dims({'n_components':'time'}) 
        grid_len = len(mean_DWT_pred[1])

        month_sim_pred = np.empty((0,grid_len),dtype=object)
        month_sim_dates = np.empty((1,0),dtype=object)
        
        for y in range(int(DWT_bmus['time.year'][0]),int(DWT_bmus['time.year'][-1])+1):
            yr_pred =DWT_bmus.sel(time = DWT_bmus['time.year']== y)

            for m in range(1,13):
                m_pred = yr_pred.sel(time = yr_pred['time.month']== m)
                stacked_pred=np.empty((0,grid_len),dtype=object)
                if len(m_pred.time)>0: # if the month has data in it:

                    for d in np.unique(m_pred['sorted_bmus_storms']):
                        dwt_pred = m_pred.sel(time = m_pred['sorted_bmus_storms']==d)
                        num_times_DWT = int(dwt_pred['sorted_bmus_storms'].count())            
                        stacked_pred = np.append(stacked_pred,np.tile(mean_DWT_pred[d],(num_times_DWT,1)),axis=0)

                

                    mean_stacked_pred = np.nanmean(stacked_pred,0) # find the mean of the month
                    temp = mean_stacked_pred.reshape(1,len(mean_stacked_pred)) - mean_month_pred[m] # remove mean of each month (seasonal signal)
                    month_sim_pred = np.append(month_sim_pred, temp,axis=0)
                    month_sim_dates = np.append(month_sim_dates,datetime(y,m,1))

        month_sim_pred_xr = xr.Dataset(coords = {'time': month_sim_dates},
                                       data_vars = dict(month_sim_pred=(['time','latitude'],
                                                                          np.array(month_sim_pred, dtype=np.float64))))
        print(month_sim_pred_xr)
    
    elif mode == 'sim':
    
        grid_len = len(mean_DWT_pred[1])
        for a in DWT_bmus.n_sim:
            print('working on sim {}'.format(a.values))
            
            month_sim_pred_a = np.empty((0,grid_len),dtype=object)
            month_sim_dates = np.empty((1,0),dtype=object)
            
            DWT_ = DWT_bmus.sel(n_sim=a)
            
            for y in range(int(DWT_['time.year'][0]),int(DWT_['time.year'][-1])+1):
                yr_pred =DWT_.sel(time = DWT_['time.year']== y)

                for m in range(1,13):
                    m_pred = yr_pred.sel(time = yr_pred['time.month']== m)
                    stacked_pred=np.empty((0,grid_len),dtype=object)

                    if len(m_pred.time)>0: # if the month has data in it:
                        for d in np.unique(m_pred['evbmus_sims']):
                            dwt_pred = m_pred.sel(time = m_pred['evbmus_sims']==d)
                            num_times_DWT = int(dwt_pred['evbmus_sims'].count())            
                            stacked_pred = np.append(stacked_pred,np.tile(mean_DWT_pred[d],(num_times_DWT,1)),axis=0)

                        mean_stacked_pred = np.nanmean(stacked_pred,0) # find the mean of the month
        #                 print(mean_stacked_pred[0])
        #                 print(mean_month_pred[m][0])
                        temp = mean_stacked_pred.reshape(1,len(mean_stacked_pred)) - mean_month_pred[m] # remove mean of each month (seasonal signal)
        #                 print(temp[0])
        #                 print()
                        month_sim_pred_a = np.append(month_sim_pred_a, temp,axis=0)
                        month_sim_dates = np.append(month_sim_dates,datetime(y,m,1))
        
            if 'month_sim_pred' in locals():
                month_sim_pred_a = np.reshape(np.array(month_sim_pred_a,dtype=np.float64),(np.shape(month_sim_pred_a)[0],np.shape(month_sim_pred_a)[1],1))
                month_sim_pred = np.concatenate([month_sim_pred,np.array(month_sim_pred_a,dtype=np.float64)],axis = 2)
                print(np.shape(month_sim_pred))

            else:    
                month_sim_pred = np.reshape(np.array(month_sim_pred_a,dtype=np.float64),(np.shape(month_sim_pred_a)[0],np.shape(month_sim_pred_a)[1],1))
                print(np.shape(month_sim_pred))


        month_sim_pred_xr = xr.Dataset(data_vars = dict(month_sim_pred=(['time','latitude','n_sim'],month_sim_pred)),
                                        coords = {'time': month_sim_dates, 'n_sim':DWT_bmus.n_sim},)
        print(month_sim_pred_xr)

    
    else:
        print('unknown mode')

    return month_sim_pred_xr



def pred_field_to_PCs(month_sim_pred_fields,local_pred,mode):
    """ 
    this function converts SLP fields to PCs using the EOF calculated from the historical period
    """
    if mode == 'hist':
        
        # standardize/ preprocess data (z-score) same way initial PCs were
        month_sim_pred = month_sim_pred_fields['month_sim_pred'].values
        predmean = np.nanmean(month_sim_pred,0)
        predstd = np.nanstd(month_sim_pred,0)
        [time,ngrids] = month_sim_pred.shape
        pred_temp = (month_sim_pred - np.tile(predmean,(time,1)))/(np.tile(predstd,(time,1)))
        
        pred_eof = local_pred['monthlyPCA']['mEOF']
        pred_eof = np.array(pred_eof[0,0],dtype=np.float64)

        # transform pred (SST or SLP) spatial fields into PCs using the EOFs (temporal variance)
        local_sim_PCs = np.linalg.lstsq(pred_eof,pred_temp.conj().T)[0].T
        # return in xarray format
        local_sim_PCs_xr = xr.Dataset(data_vars = dict(local_sim_PCs=(['time','PCs'],local_sim_PCs)),
                                    coords = {'time': month_sim_pred_fields.time},)
    else:
        for s in month_sim_pred_fields.n_sim:                                     
              # standardize/ preprocess data (z-score) same way initial PCs were
            month_sim_pred = month_sim_pred_fields.sel(n_sim=s)['month_sim_pred'].values
            predmean = np.nanmean(month_sim_pred,0)
            predstd = np.nanstd(month_sim_pred,0)
            [time,ngrids] = month_sim_pred.shape
            pred_temp = (month_sim_pred - np.tile(predmean,(time,1)))/(np.tile(predstd,(time,1)))

            pred_eof = local_pred['monthlyPCA']['mEOF']
            pred_eof = np.array(pred_eof[0,0],dtype=np.float64)

            # transform pred (SST or SLP) spatial fields into PCs using the EOFs (temporal variance)
            local_sim_PCs_s = np.linalg.lstsq(pred_eof,pred_temp.conj().T)[0].T 
            #stack in 3d array before putting in xarray format
            if 'local_sim_PCs' in locals():
                local_sim_PCs_s = np.reshape(local_sim_PCs_s,(np.shape(local_sim_PCs_s)[0],np.shape(local_sim_PCs_s)[1],1))
                local_sim_PCs = np.concatenate([local_sim_PCs,np.array(local_sim_PCs_s,dtype=np.float64)],axis = 2)
                     
            else:    
                local_sim_PCs = np.reshape(local_sim_PCs_s,(np.shape(local_sim_PCs_s)[0],np.shape(local_sim_PCs_s)[1],1))


        local_sim_PCs_xr = xr.Dataset(data_vars = dict(local_sim_PCs=(['time','PCs','n_sim'],local_sim_PCs)),
                                    coords = {'time': month_sim_pred_fields.time, 'n_sim':month_sim_pred_fields.n_sim},)
        
        

    return local_sim_PCs_xr
