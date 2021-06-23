import csv
import json

'''
Read .csv file consisting partly of standard csv format and "dictionary" format.
Output in .json format
'''


csvfile = open('../data/TestReport_fail_example.csv', 'r')
jsonfile = open('Output_failed_v1.json', 'w')

'''
reader ist der iterator ueber das .csv file
'''
reader = csv.reader(csvfile)


'''
Einfach nur ein paar Variablen inizialisieren...
'''
counter = 0
thisdict = {}
list_output = []
LineNumber =0
last_zero=0
vector_fields = []
keyname = ""

'''
Iteriere ueber die Reihen im .csv file
row[0] ; row[1] ; row[2] ; ....
'''
for row in reader:
    '''
    Das ist hier eine Art, um "Separatoren"/Bloecke im csv file zu erkennen (leere Reihen)
    (wahrscheinlich haesslich, funktioniert hier aber...)
    Merkt sich die nummer der letzten leeren Reihe im csv file
    '''
    if len(row) == 0:
        last_zero = reader.line_num
    '''
    Falls die Zeile nicht leer ist und die Reihe weniger als 4 Spalten hat
    (reader.line_num < 3 sorgt dafuer dass die nutzlose Ueberschrift nicht beruecksichtigt wird)
    '''
    if len(row) > 1 and reader.line_num > 3 and len(row) < 4:
        """
        Die Bloecke im .json file sollen sich nach den Bloecken im csv file richten, die immer mit einem 
        "Titel" beginnen
        {
            Titel : {
                "Name" : "Max Mustermann",
                "Datum" : "xx.xx.xxxx",
                .....
        
            }
        },...
        

        Das hier ist ziemlich "erfolgsorientiert" (wahrscheinlich haesslich): 
        - Die Zeile wird eingelesen. Im "Dictionary" teil des .csv habe ich immer folgendes Format
        fieldname ; result  (= row[0] ; row[1])
        (also Name ; Max Mustermann)
        - Ein counter registriert einfach nur ob das das erste Element "Title" ist, das eingelesen wird
        - Das Element neben "Title" ist das key im .json dictionary. Der "value" des Dictionary sind die Key-Value
        Paare, die folgen (bis zur naechsten Leerzeile) (also der nachfolgende Block im .csv file)
        - Sobald der Code in der naechsten "Title"-Zeile angekommen ist, werden die key-Value paar des vorherigen 
        Absatzes in ein Dictonary gedumpt
        - Das kann nur gemacht werden, wenn das dictionary schon existiert (also counter > 0 ist), deswegen der counter
        """
        fieldname=row[0]
        result = row[1]
        if "Title" in fieldname:
            if counter > 0:
                # Dump the dictionary in the nested dictionary "arr_outputData".
                # This step is performed after the array is created ("if counter > 0:")
                # Array is created in "else"
                if len(thisdict) != 0:
                    mydict = {keyname : thisdict}
                    list_output.append(mydict)
                    thisdict ={}

            keyname = result

            counter = counter + 1
        else:
            thisdict[row[0]] = row[1]

    #
    #Jetzt kommt der "csv-Teil" des csv-files (also der Teil im wahren csv format)
    #Wenn die Zeile mehr als vier spalten & Ueberspringe die ersten drei (nutzlosen) Zeilen

    elif reader.line_num > 3 and len(row) > 4:
        fieldname = row[0]
        print(fieldname)
        '''
        "Name" oder "#" sind immer am Block-Anfang
        '''
        if '#' in fieldname or "Name" in fieldname:
            nr_fields = len(row) #Anzahl der Spalten
            vector_fields.clear()
            vector_fields = []
            for i in range(nr_fields): #iteriere ueber die Spalten und merke die Header
                vector_fields.append(row[i])
            LineNumber = reader.line_num #Variable, die einfach nur registriert, ob ein Block gefunden wurde
        else:
            '''
            Wenn ein Block mit "Name" oder "#" gefunden wurde, 
            iteriere vom Blockanfang bis zur naechsten Leerzeile, die das Blockende signalisisert
            Speichere den Titel und den zugehoerigen Wert in einer Zeile in ein Dictionary ab
            (fuer jede Zeile = Messwert ein Dictionary object)
            '''
            if LineNumber != 0 and reader.line_num > LineNumber and last_zero < LineNumber:

                list_Data = []
                list_Data.clear()
                nr_fields = len(row)
                for i in range(nr_fields): #Iteriere ueber Spalten
                    list_Data.append(row[i])
                array_dict = {}
                for j, co in enumerate(vector_fields):
                    array_dict[co] = list_Data[j]
                arr_helper = {}
                arr_helper[keyname] = array_dict
                list_output.append(arr_helper)


'''
jetzt speichere das gesamte Dictonary in ein json file
'''


str_ = json.dumps(list_output, indent=4, separators=(',', ':'))
jsonfile.write(str_)


