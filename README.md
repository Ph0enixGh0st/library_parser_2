# Library Parser
The script downloads books and saves them to the script folder.

### How to install
Using GitHub CLI:
```bash
gh repo clone Ph0enixGh0st/library_parser_2
```
Or download and unpack ZIP file from GIT Hub repository: https://github.com/Ph0enixGh0st/library_parser_2.git

# Prerequisites
Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

# tululu.py and how to run it
The script downloads books from tululu.org and saves them to 'books' folder from where the script is run.
When running the script book text files and book cover image files will be created.

In order to start the script please run the following command in terminal/cmd/powershell:

```bash
python3 parse_tululu_category.py --start_page 0 --end_page 2
```

'--start_page' argument is the collection page number starting from which the script will begin to fetch the books from tululu website.

'--end_page' argument is the collection page number starting to which the script will fetch the books from tululu website.

'--skip_imgs' argument will turn off book covers download if 'True' is specified

'--skip_txt' argument will turn off book texts download if 'True' is specified

'--dest_folder' argument will change the books download destionation folder

'--json_path' argument will change the JSON books about file destionation folder


### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
