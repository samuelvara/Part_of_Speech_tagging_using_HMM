import sys, os
def accuracy_from_txt_files(dev_path, op_path, language='default'):
    dev_lines = load_file(dev_path)
    pred_lines = load_file(op_path)
    print('Results for: '+language)
    calculate_accuracy(dev_lines, pred_lines,language)

def load_file(file):
    f = open(file, 'r')
    lines_list = []
    for line in f.readlines():
        cur_line = []
        for word_tag in line.replace('\n', '').split(' '):
            word = word_tag.rsplit('/', 1)[0]
            tag = word_tag.rsplit('/', 1)[1]
            cur_line.append((word, tag))
        lines_list.append(cur_line)
    return lines_list

def calculate_accuracy(dev_lines, pred_lines,language):

    difference = len(dev_lines) - len(pred_lines)

    if difference > 0:
        print('Output file has: '+ str(difference) + ' lesser lines than pred file')
        return
    elif difference < 0:
        print( 'Output file has: '+ str(abs(difference)) + ' lesser lines than pred file') 
        return 
    
    line_no = 0
    denominator = 0
    numerator = 0
    for i in range(len(dev_lines)):
        line_no += 1
        difference = len(dev_lines[i]) - len(pred_lines[i])
        if difference > 0:
            print('Line '+str(line_no)+' has '+ str(difference)+ ' lesser tokens than pred file')
            return
        elif difference < 0:
            print('Line '+str(line_no)+' has '+ str(difference)+ ' more tokens than pred file')
            return

        for j in range(len(dev_lines[i])):
            denominator += 1
            if dev_lines[i][j][0] == pred_lines[i][j][0]:
                if dev_lines[i][j][1] == pred_lines[i][j][1]:
                    numerator += 1
                # else:
                #     print("Mismatch: ",dev_lines[i][j],"Predicted:",pred_lines[i][j],i,j)
            else:
                print('Words dont match at position: '+ str(j))
                continue
    print('Total no of words: '+ str(denominator))
    print('Words predicted correctly: '+ str(numerator))
    print('Accuracy: '+ str(float(numerator)/denominator*100)+"%")
    accuracy=float(numerator)/denominator
    if(language=="Italian"):
        baseline=0.89385
        reference=0.94239
    else: 
        baseline=0.86268
        reference=0.91889
    grade=0
    print('Baseline: '+ str(baseline*100))
    print('Reference: '+str(reference*100))
    if accuracy<baseline:
        grade=accuracy
    elif baseline<accuracy and accuracy<reference:
        grade=baseline+(1-baseline)*(accuracy-baseline)/(reference-baseline)
    else:
        grade=1
        print("You are done!!")
    print('Grade: '+ str(grade*10))




if __name__=='__main__':
    test=sys.argv[1]
    output=sys.argv[2]
    language=sys.argv[3]
    accuracy_from_txt_files(test,output,language)

