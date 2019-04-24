import os,sys
import os,sys
import subprocess
import shutil

def mergefiles(flist,outfile):
	with open(outfile, "wb") as fout:
        	for f in flist:
                	with open(f, "rb") as infile:
                        	fout.write(infile.read())
		    	fout.write('\n')



if __name__ == "__main__":

	#Get current working directory
	curr=os.getcwd() 
	pkgdir="/data/zusers/vangaves/BIN/SPRING"
	seqdir=sys.argv[1] # folder containing ligand and receptor sequences
	seq=sys.argv[2] #Name for the complex
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
