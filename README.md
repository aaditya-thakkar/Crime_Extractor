# User’s manual for Crime Information Extraction :


Crime_Extractor uses Snorkel, Python 2.7 and requires a few python packages which can be installed using pip.

```
pip install --requirement python-package-requirement.txt
```

Note that you may have to run pip2 if you have Python3 installed on your system, and that sudo can be prepended to install dependencies system wide if this is an option and the above does not work.

Finally, enable ipywidgets:

```
jupyter nbextension enable --py widgetsnbextension --sys-prefix
```


## Installing Numbskull + NUMBA

Snorkel currently relies on numbskull and numba, which occasionally requires a bit more work to install! One option is to use conda as above. If installing manually, you may just need to make sure the right version of llvmlite and LLVM is installed and used; for example on Ubuntu, run:

```
apt-get install llvm-3.8
LLVM_CONFIG=/usr/bin/llvm-config-3.8 pip install llvmlite
LLVM_CONFIG=/usr/bin/llvm-config-3.8 pip install numba
```
Finally, once numba is installed, re-run the numbskull install from the python-package-requirement.txt script:
```
pip install git+https://github.com/HazyResearch/numbskull@master
```

After installing, just run:
```
./run_jupyter.sh
```

Once you run the script, Jupyter notebook will start running on `localhost:8888`, go to `localhost:8888` and create a new python2 notebook. A jupyter shell will be opened and there you can work on with your further code and compiling and running it.


## Important points:
 
* The articles on which we are working are stored at /snorkel/tutorials/intro/articles.tsv. These articles are converted to .tsv files, which means they are stored as tab separated  values of id and document text. This crime extractor parses and generates corpus from .tsv files. Hence it is mandatory to first convert the articles text files into a tab separated values file.

* In the snorkel root directory shown in localhost:8888, there’s a file named extractor.py, which contains the whole logic of the code. Click on the file and the code will appear in a python jupyter shell.

* After that, we can run the code by pressing “Play” button in the taskbar and pause/stop the execution too.

* When we run the code, it takes a while to make a corpus from articles.tsv file, after which NER, Ngrams and LFs are performed on it. 
* It is needed to remove snorkel.db file from the root every time we run the candidate extractor, because a new copy of it is made every time we run it. Hence keeping out the code from rebuild, it is advisable to remove snorkel.db file and let it be created on runtime.
* Once we run the code, final output is stored in a excel sheet in the tuples of the form (document_id, date, crime_type, crime_locations). This excel file named output.-final xlsx is in the root directory of the snorkel. It gets updated everytime we run the code.
















