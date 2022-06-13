# Record of Data Acquisition and Manipulation

## Initial Acquisition

**Date**: 2022-07-10<br/>
**Files**: ner.csv, ner_dataset.csv<br/>
**Source**: [Kaggle entity annotated corpus](https://www.kaggle.com/datasets/abhinavwalia95/entity-annotated-corpus)<br/>


**Date**: 2022-06-12<br/>
**Files**: all-news-data-2-1.zip<br/>
**Source**: [components one datasets - news articles and essays](https://components.one/datasets/all-the-news-2-news-articles-dataset/)<br/>
**Type**: ZIP,CSV<br/>
**Size**: 3.4 GB compressed, 8.8 GB uncompressed<br/>
**Created by**: Andrew Thompson<br/>
**Date added**: 2020-03-04<br/>
**Date modified**: 2020-03-04<br/>

### Processing consideration

**Date**: 2022-06-13<br/>
**Files**: all-news-data-2-1.csv<br/>
**Column name applied**: idx,article_idx,date,year,month,day,author,title,article,url,section,publication<br/>
**Column name file**: ,Unnamed: 0,date,year,month,day,author,title,article,url,section,publication<br/>
**Exclude rows**: the row 0 and 2,324,812 was exclude from the dataset. the line 0 contains None values for columns headers.
line 2,324,812 contains string columns in a numeric column article_idx.<br/>
