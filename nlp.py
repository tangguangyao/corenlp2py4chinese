# -*- coding: utf-8 -*-
#export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home
#export JRE_HOME=/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home
#export JDK_HOME=/System/Library/Frameworks/JavaVM.framework/Versions/Current
import os
import json
import socket
from socket import error as SocketError
os.environ['CLASSPATH'] = "./nlp_lib/slf4j-api.jar:./nlp_lib/slf4j-simple.jar:./nlp_lib/stanford-chinese-corenlp-2016-01-19-models.jar:./nlp_lib/stanford-corenlp-3.6.0-models.jar:./nlp_lib/stanford-corenlp-3.6.0.jar:./nlp.jar"
from jnius import autoclass

Processor = autoclass('nlp.Processor')
nlpProcessor = Processor()

nlpProcessor.init()

NLP_Port = 5006;
NLP_IP = '172.100.100.197';
# NLP_IP = '127.0.0.1';
BUFFER_SIZE = 1024

# filter the invalid word by NLP POSTagger Annotator
# [1]     AD    副词  Adverbs
# [2]     AS    语态词  — 了
# [3]     BA    把
# [4]     CC    并列连接词（coordinating conj）
# [5]     CD    许多(many),若干（several),个把(a,few)
# [6]     CS    从属连接词（subording conj）
# [7]     DEC   从句“的”
# [8]     DEG   修饰“的”
# [9]     DER   得 in V-de-const, and V-de R
# [10]    DEV   地 before VP
# [11]    DT    限定词   各（each),全(all),某(certain/some),这(this)
# [12]    ETC   for words 等，等等
# [13]    FW    外来词 foreign words
# [14]    IJ     感叹词  interjecton
# [15]    JJ     名词修饰语
# [16]    LB    被,给   in long bei-const
# [17]    LC    方位词
# [18]    M     量词
# [19]    MSP   其他小品词（other particle） 所
# [20]    NN    口头名词、others
# [21]    NR    专有名词
# [22]    NT    时间名词  （temporal noun）
# [23]    OD    序数（ordinal numbers）
# [24]    ON    拟声法（onomatopoeia）
# [25]    P      介词   （对，由于，因为）(除了 “把”和“被”)
# [26]    PN    代词
# [27]    PU    标定符号
# [28]    SB    in short bei-const 被，给
# [29]    SP    句尾语气词
# [30]    VA    表语形容词（predicative adjective）
# [31]    VC    是
# [32]    VE    有（have，not have ,有，无，没，表示存在的词
# [33]    VV    情态动词、  动词、possess/拥有 ，rich/富有,具有

# DEC AD CC DEC DEG DT ETC IJ ON P SP VV

def filterInvalidWord(sentence):
    text = "";
    # "CC" "VV"
    InvalidList = ["DEC", "AD", "DEC", "DEG", "DT", "ETC", "IJ", "ON", "P", "SP", "PN"]
    # InvalidList = ["DEC", "AD", "DEC", "DEG", "DT"]
    for word in sentence:
        if not word["pos"] in InvalidList:
            text += word["word"]
    return text

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((NLP_IP, NLP_Port))
while 1:
    s.listen(1)
    conn, addr = s.accept()
    print('Connection address:' + str(addr))
    while 1:
        try:
            data = conn.recv(BUFFER_SIZE)
        except SocketError as e:
            break
        if not data:
            break
        # print(data)
        result = nlpProcessor.analyze(data)
        # print(result)
        result = json.loads(result)
        # print(result)
        sentence = filterInvalidWord(result['sentence'])
        # print("output:" + sentence)
        conn.send(sentence.encode('utf-8'))
    conn.close()
