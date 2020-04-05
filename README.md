https://github.com/LineG/ADA_472_P2/
> Above is the link to our GitHub repo

### ADA_472
AI _ WINTER 2020 Concordia University
### Project 2
The current version is only for delivrable 1:
- N-Gram models with 3 variables as input: size, vocabulary, smoothing

- BYOM fixed input that are optimized

### Team Members
- Line Ghanem 27280076
- Anthony Iatropoulos 40028246
- Mikael Samvelian 40003178

## How to run our project:
1. We are using python 3.7

2. To run the models with only three variables run: 
- make sure u are in ADA_472_P2
- change the laste line in test.py to run(V, n, d)

> python3 test.py

3. to run our own model:

> python3 test_byom.py

4. in the models folder you can see the n_gram that was built

5. in the ModifiedDataSet folder the eval and trace files are provided:
- For test.py and V=1 n=2 d=0.1 --> eval_1_2_0.1.txt and trace_1_2_0.1.txt
- For BYOM test_byom.py --> eval_MyModel.txt and trace_MyModel.tx
