# ZING
ZING is a method to identify and combine high-confidence protein-protein complex structure predictions of a template-free method (ZDOCK) with a template-based method (SPRING). 

# USAGE
python ZING.py [-h] [-zdir zdres] [-sdir spres]

Arguments:

  -h, --help   show this help message and exit
  
  -zdir zdres  ZDOCK results directory (default: current directory)
  
  -sdir spres  SPRING results directory (default: current directory)

Note: 
'zdres' should be the directory that contains the zdock output files along with the top 10 complexes (complex.1.pdb, complex.2.pdb...)
'spres' should be the directory that contains the SPRING results including the TemplateSummary.txt file and the Models folder (model1.pdb, model2.pdb...) 


# INPUT DATA for ZING
ZING requires results from ZDOCK and SPRING for the same set of proteins. 

ZDOCK and SPRING are implemented as webservers or you can also download a copy for use locally on your machine. 
To use the webservers or to download the softwares, an academic email id is required. 

## WEBSERVER:
The ZDOCK webserver is hosted at:
http://zdock.umassmed.edu
- Requires query protein structures as input 
- Provides the zdock.out file and the top 10 complexes as output. 

The SPRING webserver is hosted at:
https://zhanglab.ccmb.med.umich.edu/spring/
- Required query protein sequences as input
- Provides a folder with the TemplateSummary file and the templates used and the models predicted as output. 

After the results become available, please use script ZING.py (see #USAGE above) to generate the final list of predictions. 


# OUTPUT from ZING
## FILE: ZING_combined10.txt
- Shows which predictions from each method were included in the combined list. 
- e.g. s3 -> third prediction from SPRING, z4 -> 4th prediction from ZDOCK, N1,N2... indicate the ranks for ZING. 

## FOLDER: ZING_Preds
- Contains the top 10 predictions obtained by combining results of ZDOCK and SPRING. (zing.1.pdb, zing.2.pdb ....) 

# EXAMPLE
Test case: 1ACB. 
Inputs: 1ACB_ZDOCK directory with results from ZDOCK
	1ACB_SPRING/1ACBA-1ACBB/SPRING  directory with results from SPRING
Usage:
python ZING.py -zdir 1ACB_ZDOCK/ -sdir 1ACB_SPRING/1ACBA-1ACBB/SPRING/

Output: ZING_combined10.txt and ZING_Preds folder. 

