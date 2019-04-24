import os,sys
import math

def logistic_regression_score(features, coeffs):
	if len(coeffs) != len(features)+1:
		print ("Insufficient coeffs for features")
		return(1)
	LR=coeffs[0]
	for i in range(1,len(coeffs)):
		LR=LR+features[i-1]*coeffs[i]
	PLR=1/(1+math.exp(-LR))
	return(PLR)
	
def main():
	#SPRING modscore coefficients
	#k_0  + k_1*Coverage + k_2*E
	k=[-14.23,12.48, 0.18] 
	curr=os.getcwd()
	s=sys.argv[1] #SPRING results directory name
	fmodname=s+'/'+s+'A'+'-'+s+'B/SPRING/ModelSummary.txt'
	fout=open(fmodname,'wb')
	fname=s+'/'+s+'A'+'-'+s+'B/SPRING/TemplateSummary.txt'
	with open(fname,'rb') as fin:
		header=fin.readline()
		header=header[0:-1]+' {:10s}'.format('modscore')+'\n'
		fout.write(header)
		#Get column indices for response and model scores
		print header
                h=header.split()
                indm=h.index('modscore')-1 # -1 because second column name has a space in the header by default (Complex Template)
                indc=h.index('Coverage')-1
                inde=h.index('Dfire')-1
		for line in fin:
			if line[0:4]!='DONE':
				l=line.split()
				modscore=logistic_regression_score([float(l[indc]),float(l[inde])],k)
				wline=line[0:-1]+' {:10.3f}'.format(modscore)+'\n'
				fout.write(wline)
	fout.close()
	
if __name__=="__main__":
	sys.exit(main())
