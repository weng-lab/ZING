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
