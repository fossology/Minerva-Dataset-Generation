import re
import os

def splitter(file,dirname):
    
    history = []
    with open(file, 'r', encoding= 'unicode_escape') as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    text = " ".join(content)
    content = text.split(". ")
    content = [x.strip() for x in content]
    para = ""
    for comb  in range(1,len(content)):
        for i in range(0, len(content)-comb+1, comb):
            if len(history)>1000:
                history = list(set(history))
                if len(history)>1000:
                    break
            para = para  + " " +  content[i]
            para = re.sub("\s\s+" , " ", para)
            para = para.strip()
            if para not in history:
                history.append(para)
    history = list(set(history))
    generate_files(history,dirname)

                
def generate_files(history,dirname):
    counter = 0
    os.makedirs(dirname, exist_ok=True)
    for texts in history:
        counter+=1
        name = dirname + '-{}.txt'.format(counter)
        with open(os.path.join(dirname,name), 'w', encoding= 'unicode_escape') as o1:
                    o1.write(texts)

def main(path):
    for roots, dirs, files in os.walk(path,topdown=True):
        for name in files:
            dirname = os.path.splitext(name)[0]
            file = os.path.join(path,name)
            splitter(file,dirname)    

if __name__ == "__main__":
    main(path)
