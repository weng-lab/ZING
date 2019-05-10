import argparse
import sys,os
import numpy as np
import subprocess
import time
import shutil
from functools import wraps
from collections import defaultdict
import math

def mergefiles(flist,outfile):
	with open(outfile, "wb") as fout:
        	for f in flist:
                	with open(f, "rb") as infile:
                        	fout.write(infile.read())
		    	fout.write('\n')



def submit_SPRING(jobname):
	#Get current working directory
	curr=os.getcwd() 
	pkgdir="/data/zusers/vangaves/BIN/SPRING"
	seqdir=sys.argv[1] # folder containing ligand and receptor sequences
	seq=jobname #Name for the complex
	seq1='receptor.seq'
	seq2='ligand.seq'
	if os.path.exists(seq):
		print "removing directory"
		shutil.rmtree(seq)
	if not os.path.exists(seq):
		os.makedirs(seq)
	mergefiles([seqdir+'/'+seq1,seqdir+'/'+seq2],seq+'/seq.fasta')
	command='nohup time '+pkgdir+'/runSPRING.pl'+' -seqname '+seq+' -datadir '+seq+' > '+seq+'/nohup.out &'
	subprocess.call(command, shell=True)


def submit_ZDOCK(jobname):
	#Get current working directory
	curr=os.getcwd() 
	pkgdir='/data/zusers/vangaves/BIN/zdock3.0.2_linux_mpi_compiled'
	structdir=sys.argv[1] # folder containing ligand and receptor structures
	structcomp=sys.argv[2] #Name for the complex folder
	receptor=sys.argv[3]
	ligand=sys.argv[4]
	if os.path.exists(structcomp):
		print "removing directory ", structcomp
		shutil.rmtree(structcomp)
	if not os.path.exists(structcomp):
		os.makedirs(structcomp)
	#mergefiles([seqdir+'/'+seq1,seqdir+'/'+seq2],seq+'/seq.fasta')
	command='nohup mpiexec -n 16 '+pkgdir+'/zdock  -R '+receptor+' -L '+ligand+' -o zdock.out -F & > nohup.out'
	subprocess.call(command, shell=True)

def logistic_regression_score(features, coeffs):
	if len(coeffs) != len(features)+1:
		print ("Insufficient coeffs for features")
		return(1)
	LR=coeffs[0]
	for i in range(1,len(coeffs)):
		LR=LR+features[i-1]*coeffs[i]
	PLR=1/(1+math.exp(-LR))
	return(PLR)
	
def SPRING_modelscores(spdir):
	#SPRING modscore coefficients
	#k_0  + k_1*Coverage + k_2*E
	k=[-14.23,12.48, 0.18] 
	curr=os.getcwd()
	s=spdir #SPRING results directory name
	fmodname=os.path.join(s,'ModelSummary.txt')
	fout=open(fmodname,'wb')
	fname=os.path.join(s,'TemplateSummary.txt')
	with open(fname,'rb') as fin:
		header=fin.readline()
		header=header[0:-1]+' {:10s}'.format('modscore')+'\n'
		fout.write(header)
		#Get column indices for response and model scores
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
	

def pooling_nocutoff_zors(fname,outname,zdprob,nmax):
	#Get column indices for response and model scores
	with open(fname,'rb') as fin: 
		line=fin.readline()
		l=line.split()
		mcol=l.index('#')
		indm=l.index('modscore')-1 #Complex Template is two columns in the header
	#Number of predictions and cut off values used
	npred=[10]
	header=''
	writeline=''
	#Outfile
	with open(fname,'rb') as fin, open(outname,'wb') as fout:

		for tot in range(0,nmax):
        		header=header+'{:6s}'.format('N'+str(tot+1))
		header=header+'\n'
		fout.write(header) 
		#Outfile
		splr=[]
		mnum=[]
		#seqrms={}  #Save IRMSD for each model for a particular sequence
		with open(fname,'rb') as fin:
                	line=fin.readline()
                	for line in fin:
                        	l=line.split()
				splr.append(float(l[indm]))	
				mnum.append('s'+l[mcol])

		#ZDOCK
		zdp=0
		znum=['z'+str(i) for i in range(1,len(zdprob)+1)]
		#Combine ZDOCKprob and SPLR lists
		spool=splr+zdprob
		#npool=['s']*len(splr) + ['z']*len(zdprob)
		npool=[ s for s in mnum]+[z for z in znum]
		#irmsdpool=irmsdlr+irmsdzd
                order=[i[0] for i in sorted(enumerate(spool), key=lambda x:x[1], reverse=True)]
		spool=[spool[i] for i in order]
		#irmsdpool=[irmsdpool[i] for i in order]
		npool=[npool[i] for i in order]
		for n in range(0,nmax):
		  		writeline=writeline+' '+'{:5s}'.format(str(npool[n]))
		writeline=writeline+'\n'
		fout.write(writeline)

	return(npool)	



def parse_args():
	#Using argument parser for getting inputs. 
	parser = argparse.ArgumentParser(description='Run ZING pipeline (a combination of ZDOCK and SPRING)')
	parser.add_argument('-zdir',metavar='zdres',default=os.getcwd(),help=' ZDOCK results directory (default: current directory)')
	parser.add_argument('-sdir',metavar='spres',default=os.getcwd(),help=' SPRING results directory (default: current directory)')
    	args=parser.parse_args()
	return args

def create_ZINGlist_models(npool,spres,zdres):
	spres=os.path.join(spres,'Models')
	if os.path.exists('ZING_Preds'):
        	print "Removing the existing directory ZING_Preds\n"
		raw_input("Press Enter to continue... \n Use ctrl+C to quit")
                shutil.rmtree('ZING_Preds')
	os.mkdir('ZING_Preds')
	fname=[]
	for p in npool:
		if p[0]=='s':
			mnum=p[1:]
			fname.append(os.path.join(spres,'model'+mnum+'.pdb'))
		elif p[0]=='z':
			mnum=p[1:]
			fname.append(os.path.join(zdres,'complex.'+mnum+'.pdb'))
	zing=1
	for f in fname:
		shutil.copyfile(f,os.path.join('ZING_Preds','zing'+str(zing)+'.pdb'))
		zing=zing+1


#################### MAIN ####################
def main():
	args=parse_args()
	zdres=args.zdir
	spres=args.sdir

	SPRING_modelscores(spres)
	SPres=sys.argv[1] #Folder with SPRING results
	ZDres=sys.argv[2] #Folder with ZDOCK results
	Nmax=10
	
	#Calculate zdprob
	npred=range(1,101)
	#Using top 500 to fit
	a=0.082; b=0.023; S=0.018
	zdprob=[round(a*math.exp(-S*n)+b, 3) for n in npred]
	
	fmodname=spres+'/ModelSummary.txt'
	outfile='ZING_combined'+str(Nmax)+'.txt'
        npool=pooling_nocutoff_zors(fmodname,outfile,zdprob,Nmax)

	create_ZINGlist_models(npool[0:10],spres,zdres)
    	helpmessage='For help use:\npython ZING.py -h \n'

	
if __name__ == "__main__":
	sys.exit(main())
