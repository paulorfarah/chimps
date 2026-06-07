import re

import pandas as pd


def concat_method(row):
    method_name = row['class'] + '.' + row['method']
    method_name = method_name.replace('/0', '()')
    # method_name = method_name.replace('/')

    method_name = re.sub('\/[0-9]+\[', '(', method_name)
    method_name = re.sub('\]$', ')', method_name)
    method_name = re.sub('\<[a-zA-Z0-9.]+\>', '', method_name)

    m = re.search('\([a-zA-Z0-9\._,\[\]]+\)$', method_name)
    if m:
        params = []
        p = re.findall('[a-zA-Z0-9\._\[\]]+,|[a-zA-Z0-9\._\[\]]+\)', m.group(0))
        for param in p:
            last = param.rsplit('.', 1)[-1]
            params.append(last.replace(',', '').replace(')', ''))

        method_name = re.sub('\([a-zA-Z0-9\._,\[\]]+\)$', '(' + ','.join(params) + ')', method_name)


    method_name = method_name.replace('$', '.')
    return method_name


def join_ck(project_name, current_hash):
    # print("CK ")
    csv_path = '../1.ck/results/' + project_name + '/' + project_name + '_' + current_hash + '_method.csv'
    # csv_path = '/home/usuario/PycharmProjects/cpmp/1.ck/results/' + project_name + '/' + project_name + '_' + current_hash + '_method.csv'
    # print(csv_path)
    method_metrics = ['file', 'class', 'method', 'constructor', 'line', 'cbo', 'cboModified', 'fanin', 'fanout', 'wmc',
                      'rfc', 'loc', 'returnsQty', 'variablesQty', 'parametersQty', 'methodsInvokedQty',
                      'methodsInvokedLocalQty', 'methodsInvokedIndirectLocalQty', 'loopQty', 'comparisonsQty',
                      'tryCatchQty', 'parenthesizedExpsQty', 'stringLiteralsQty', 'numbersQty', 'assignmentsQty',
                      'mathOperationsQty', 'maxNestedBlocksQty', 'anonymousClassesQty', 'innerClassesQty', 'lambdasQty',
                      'uniqueWordsQty', 'modifiers', 'logStatementsQty', 'hasJavaDoc']

    # metrics = ["class", "type", "cbo", "wmc", "dit", "rfc", "lcom", "tcc", "lcc", "totalMethodsQty",
    #                      "staticMethodsQty", "publicMethodsQty", "privateMethodsQty", "protectedMethodsQty",
    #                      "defaultMethodsQty", "abstractMethodsQty", "finalMethodsQty", "synchronizedMethodsQty",
    #                      "totalFieldsQty", "staticFieldsQty", "publicFieldsQty", "privateFieldsQty",
    #                      "protectedFieldsQty", "defaultFieldsQty", "visibleFieldsQty", "finalFieldsQty",
    #                      "synchronizedFieldsQty", "nosi", "loc", "returnQty", "loopQty", "comparisonsQty",
    #                      "tryCatchQty", "parenthesizedExpsQty", "stringLiteralsQty", "numbersQty", "assignmentsQty",
    #                      "mathOperationsQty", "variablesQty", "maxNestedBlocksQty", "anonymousClassesQty",
    #                      "innerClassesQty", "lambdasQty", "uniqueWordsQty", "modifiers", "logStatementsQty"]

    df = pd.read_csv(csv_path, usecols=method_metrics, sep=',', index_col=False)
    if len(df):
        df['method_name'] = df.apply(concat_method, axis=1)
    return df
