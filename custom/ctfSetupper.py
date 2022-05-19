#!/usr/bin/python3.9
import optparse
import subprocess

###########################3
#       by Cave 2022
###########################3


# Exact use of / are important here
# Suffix and prefix /'s need to be right
HOME_DIR = "/home/cave/"
CTF_FOLDER = HOME_DIR + "Documents/CTF/"
CUSTOM_TOOLING = HOME_DIR + ".tooling/custom/"
PWN_TEMPLATE = CUSTOM_TOOLING + "pwntemp.py"

with open(CUSTOM_TOOLING+"CTF_CONTEXT", "r") as f:
    CTF_CONTEXT = f.read()



def optParser():
    parser = optparse.OptionParser()
     
    # add options
    parser.add_option('-f', dest = 'file',
                      type = 'str',
                      help = 'Specify the file')
    parser.add_option('-s', dest = 'ctfContext',
                      type = 'str',
                      help = 'Specify the current ctf')
    parser.add_option('-c', dest = 'challCategory',
                      type = 'str',
                      help = 'Specify the current challenges category')
     
    (options, args) = parser.parse_args()


    if options.ctfContext:
        with open(CUSTOM_TOOLING+"CTF_CONTEXT", "w") as f:
            f.write(options.ctfContext)
            print(f"Writing {options.ctfContext} > CTF_CONTEXT")
            exit("[:)] Wrote new CTF context")

    elif options.challCategory:
        if "web" in options.challCategory.lower():
            return options.file, "web"
        elif "pwn" in options.challCategory.lower():
            return options.file, "pwn"
        elif "rev" in options.challCategory.lower():
            return options.file, "rev"
        elif "crypto" in options.challCategory.lower():
            return options.file, "crypto"
        elif "misc" in options.challCategory.lower():
            return options.file, "misc"
        elif "foren" in options.challCategory.lower():
            return options.file, "forensics"
        else:
            exit("""
        ----------
        Possible categories, you silly goose:
        web, rev, pwn, crypto, misc, and forensics
        ----------
        """)

    elif options.file:
        return options.file, None

    else:
        print(options.file)
        exit("""
        Sorry that is not a command!
        You can use -f <file> to specify a file.
        You can also use -c <category> 
        OR you can set the CTF context with
        -s <ctf>. To see all commands
        try running -h or --help!
        """)



def ctfSetup(fileName, category):
    ans = input(f"Do you want to setup? [y/n]\nCurrent context: {CTF_CONTEXT}\n") 
    if ans.lower() == "n":
        return 0
    else:
        setupEnv = CTF_FOLDER+CTF_CONTEXT
        print(f"This is your ctf setup folder: {setupEnv}\nHappy hacking!\n")

        # Ensure that folder does not exist
        folderExists = subprocess.call(["/usr/bin/test", "-e", setupEnv])
        if folderExists == 1:
            subprocess.call(["/usr/bin/mkdir", setupEnv])
            subprocess.call(["/usr/bin/mkdir", setupEnv+"/web"])
            subprocess.call(["/usr/bin/mkdir", setupEnv+"/pwn"])
            subprocess.call(["/usr/bin/mkdir", setupEnv+"/rev"])
            subprocess.call(["/usr/bin/mkdir", setupEnv+"/crypto"])
            subprocess.call(["/usr/bin/mkdir", setupEnv+"/misc"])
            subprocess.call(["/usr/bin/mkdir", setupEnv+"/forensics"])

        if category:
            catFolder = setupEnv+"/"+category+"/"+fileName.split(".")[0]
            subprocess.call(["/usr/bin/mkdir", catFolder])
            subprocess.call(["/usr/bin/mv", fileName, catFolder])


            solExists = subprocess.call(["/usr/bin/test", "-e", catFolder+"/"+"pwntemp.py"])
            if solExists == 1:
                if category == "pwn":
                    subprocess.call(["/usr/bin/cp", CUSTOM_TOOLING+"pwntemp.py", catFolder])
            
                elif category == "rev":
                    subprocess.call(["/usr/bin/cp", CUSTOM_TOOLING+"pwntemp.py", catFolder])
            
            readmeExists = subprocess.call(["/usr/bin/test", "-e", catFolder+"/"+"README.md"])
            if readmeExists == 1:
                subprocess.call(["/usr/bin/touch", catFolder+"/"+"README.md"])
        else:
            subprocess.call(["/usr/bin/mv", fileName, setupEnv])


def main(fileName, category):
    ctfSetup(fileName, category)


if __name__ == "__main__":
    file, category = optParser()

    main(file, category)
