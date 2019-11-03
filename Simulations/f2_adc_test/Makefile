CONTROLLER=PYTHON
#Directories
THESDKHOME = /tools/projects/kosta/TheSDK
TOP_ENTITY= f2_adc_test
MATLABPATH= /tools/projects/kosta/TheSDK/Simulations/f2_adc_test/Matlab
PYTHONPATH= /tools/projects/kosta/TheSDK/Simulations/f2_adc_test/Python
PICPATH= /tools/projects/kosta/TheSDK/Simulations/f2_adc_test/Pics
SLIDEPATH= /tools/projects/kosta/TheSDK/Simulations/f2_adc_test/Slides
MATLABFILE= f2adctest
PYFILE= f2adctest
DEPDIR :=.depdir
$(shell mkdir -p $(DEPDIR) >/dev/null)

#Commands
PY= bsub -K -q normal python3.6
PYL= python3.6
PYI= bsub -I python3.6
MATLAB= bsub -K -q normal matlab -nodisplay -nosplash -nodesktop
MATLABI= bsub -I matlab -nodisplay -nosplash -nodesktop
MATLABG= bsub -I -XF matlab -nosplash -desktop
TOUCH=touch -r
#You must ensure these cmdfiles update the target
MCMDFILE=$(MATLABPATH)/$(MATLABFILE).m
PYCMDFILE= $(PYTHONPATH)/$(PYFILE).py

MTARGETS=$(MCMDFILE:.m=.status) #Ensure these files are generated with matlab cmd
PYTARGETS=$(PYCMDFILE:.py=.status) #Ensure these files are generated with python cmd

ifeq ($(CONTROLLER), MATLAB)
#Create matlab dependency files from the master cmdfile
#Need to add the location paths of the matlab dependencies with addpath/genpath
#Note double quote after -r
MAKEDEPEND= bsub -I matlab -nodisplay -nosplash -nodesktop -r "addpath('$(MATLABPATH)'); \
            addpath(genpath('$(THESDKHOME)/Entities')); \
            [fList,pList]=matlab.codetools.requiredFilesAndProducts('$<');             fid=fopen('$(DEPDIR)/$(*F).txt','w');\
            for i=1:length(fList); fprintf(fid,'%s\n',char(fList(i))); end; quit;" \
            && awk '{print "$@: " $$1 }' $(DEPDIR)/$(*F).txt > $(DEPDIR)/$(*F).d && rm -f  $(DEPDIR)/$(*F).txt
endif

ifeq ($(CONTROLLER), MATLAB)
.PHONY: matlabg matlabi matlab slides all
all: matlab slides
endif

ifeq ($(CONTROLLER), PYTHON)
.PHONY: py pyl slides all
all: python slides
endif

slides: $(SLIDEPATH)/pdffiles/$(TOP_ENTITY).pdf 

ifeq ($(CONTROLLER), MATLAB)
$(SLIDEPATH)/pdffiles/%.pdf :  $(MATLABPATH)/$(MATLABFILE).status
	ln -sf $(PICPATH)/*.eps $(SLIDEPATH)/Pics/
	cd $(SLIDEPATH) && ./makearticle $(SLIDEPATH)/$(*F).tex && cd ..
endif 

ifeq ($(CONTROLLER), PYTHON)
$(SLIDEPATH)/pdffiles/%.pdf : $(PYTHONPATH)/$(PYFILE).status
	ln -sf $(PICPATH)/*.eps $(SLIDEPATH)/Pics/
	cd $(SLIDEPATH) && ./makearticle $(SLIDEPATH)/$(*F).tex && cd ..
endif

#If results are stored in the .mat file
matlab: $(MTARGETS)

$(MATLABPATH)/%.status : $(MATLABPATH)/%.m $(DEPDIR)/%.d
	$(MAKEDEPEND)
	$(MATLABI) -r ' addpath $(MATLABPATH); $(*F); quit;'


#interactive matlabsession
matlabi: $(MCMDFILE)
	$(MATLABI) -r ' addpath $(MATLABPATH); $(MATLABFILE); quit;'
    
#interactive gui open
matlabg: 
	$(MATLABG) -r ' addpath $(MATLABPATH);'

#Python submission
python: $(PYTARGETS)

$(PYTHONPATH)/%.status : $(PYTHONPATH)/%.py
	$(PYI) $(PYTHONPATH)/$(PYFILE).py

py: 
	$(PYI) $(PYTHONPATH)/$(PYFILE).py

#local Python submission
pyl: 
	$(PYL) $(PYTHONPATH)/$(PYFILE).py

clean:
	rm -f $(MATLABPATH)/*.status
	rm -f $(PYTHONPATH)/*.status
	rm -f $(SLIDEPATH)/Pics/*.eps
	rm -f $(PICPATH)/*.eps
	rm -f $(SLIDEPATH)/Pdffiles/*.pdf
	rm -rf $(DEPDIR)

ifeq ($(CONTROLLER), MATLAB)
#Semicolon is a must?
$(DEPDIR)/%.d: ;
.PRECIOUS: $(DEPDIR)/%.d

#Includes the dependency files for the cmdfiles generated
#by $(MAKEDEPEND). Make is re-run, if these are created.
#during the make
#If the include is incorrect, empty recipe does not cause recompilation
#In that case, Depfiles are considered intermediate.
include $(MCMDFILE:$(MATLABPATH)/%.m=$(DEPDIR)/%.d)
endif
