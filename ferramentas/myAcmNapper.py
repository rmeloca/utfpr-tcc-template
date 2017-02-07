import os;
import time;
import urllib2;
from urllib import FancyURLopener;

os.system("cat *.html >> ids.clump; rm *.html");

final = [];
f = open("ids.clump", 'r').readlines();
countGeral = 0;
for i in f: 
  if(len(i.split("citation.cfm?id=")) > 1):
    #retira o id do paper
    idCompleto = i.split("citation.cfm?id=")[1].split("&")[0];
    if(idCompleto[len(idCompleto) - 1:] == '\n'): continue;
    #id de papers --> 1234567.1234567
    if (len(idCompleto.split(".")) > 1):
      idParcial = idCompleto.split(".")[1];
    #id de confercias  --> 1234567
    else: idParcial = idCompleto;
    #seleciona o abstract do paper
    openerAbs = urllib2.build_opener();
    openerAbs.addheaders = [('User-agent', 'Mozilla/5.0')];
    f = openerAbs.open("http://dl.acm.org/citation.cfm?id=" + idCompleto + "&preflayout=flat");
    tmp = f.readlines();
    f.close; 
    abstract = "";
    for x in range(len(tmp)):
      if (len(tmp[x].split("<div style=\"display:inline\">")) > 1): 
        abstract = tmp[x].split("<div style=\"display:inline\">")[1]; break;
    abstract = abstract.replace("<p>", "");
    abstract = abstract.replace("</p>", "");
    abstract = " abstract = {" + abstract.split("</div>")[0] + "},\n";
    final.append(["http://portal.acm.org/exportformats.cfm?id=" + idParcial + "&expformat=bibtex", abstract]);
    countGeral += 1;
    print("Abstract number "+ str(countGeral) + "\n");
    print(abstract);
    
    
    time.sleep(5);
    

#junta os bibtex e o abstract no arquivo

count = 0;
out = open("master.bib",'w');
for i in final: 
  opener = urllib2.build_opener();
  opener.addheaders = [('User-agent', 'Mozilla/5.0')];
  f = opener.open(i[0]);
  s = f.readlines();
  f.close();
  success = 0;
  for j in range(len(s)): 
    if(len(s[j].split(" title = {"))>1): 
      s.insert(j+1,i[1]);
      success = 1;
  count += 1; 
  if(success): print("\n>>> Reference " + str(count) + " downloaded successfully! (" + str(countGeral) + " total!)\n");
  else: print("\nReference " + str(count) + " download failed! (" + str(countGeral) + " total!)\n");
  do_print = 0;
  for j in s:  
    if len(j) < 1: continue;
    if j[0] == "@": out.write(j); do_print = 1; continue;
    if j[0] == "}": out.write(j + '\n'); do_print = 0; continue;
    if do_print: 
      print j, 
      out.write(j);
  time.sleep(5);

out.close();