import re

import pandas as pd

packs = {'commons-bcel': ['examples\/', 'src\/examples\/', 'src\/java\/', 'src\/main\/java\/', 'src\/test\/'],
         'commons-io': ['src\/test\/java\/', 'src\/java\/', 'src\/main\/java\/', 'src\/test\/'],
         'junit4': ['src\/test\/java\/', 'src\/java\/', 'src\/main\/java\/', 'src\/test\/', ''],
         'pdfbox': ['src\/test\/java\/', 'src\/java\/', 'src\/main\/java\/', 'src\/test\/',
                    'ant\/src\/main\/java\/', 'examples\/src\/main\/java\/',
                    'lucene\/src\/main\/java\/', 'preflight\/src\/main\/java\/',
                    'pdfbox\/src\/main\/java\/', 'jempbox\/src\/main\/java\/',
                    'xmpbox\/src\/main\/java\/', 'fontbox\/src\/main\/java\/',
                    'fontbox\/src\/test\/java\/', 'debugger\/src\/main\/java\/',
                    'tools\/src\/main\/java\/', 'pdfbox\/src\/test\/java\/',
                    'xmpbox\/src\/test\/java\/', 'examples\/src\/test\/java\/',
                    'preflight\/src\/test\/java\/',
                    ''],
         'wro4j': ['src\/test\/java\/', 'src\/java\/', 'src\/main\/java\/', 'src\/test\/',
                   'wro4j-examples/src/main/java/', 'wro4j-maven-plugin/src/main/java/',
                   'wro4j-extensions/src/main/java/', 'wro4j-test-utils/src/main/java/',
                   'wro4j-core/src/main/java/',
                   'wro4j-examples/src/test/java/', 'wro4j-maven-plugin/src/test/java/',
                   'wro4j-extensions/src/test/java/', 'wro4j-test-utils/src/test/java/',
                   'wro4j-core/src/test/java/', ''],
         'commons-csv': ['src\/test\/java\/', 'src\/java\/', 'src\/main\/java\/', 'src\/test\/', ''],
         'easymock': ['src\/samples\/java\/',
                      'bench\/src\/main\/java\/', 'core\/src\/main\/java\/', 'core\/src\/samples\/java\/',
                      'core\/src\/test\/java\/', 'test-android\/src\/main\/java\/', 'test-deploy\/src\/main\/java\/',
                      'test-integration\/src\/main\/java\/', 'test-integration\/src\/test\/java\/',
                      'test-java8\/src\/test\/java\/', 'test-junit5\/src\/test\/java\/', 'test-nodeps\/src\/test\/java\/',
                      'test-osgi\/src\/test\/java\/', 'test-testng\/src\/test\/java\/',
                      'src\/test\/java\/', 'src\/java\/', 'src\/main\/java\/', 'src\/test\/',
                      'easymock\/src\/samples\/java\/',
                      'easymock\/bench\/src\/main\/java\/', 'easymock\/core\/src\/main\/java\/', 'easymock\/core\/src\/samples\/java\/',
                      'easymock\/core\/src\/test\/java\/', 'easymock\/test-android\/src\/main\/java\/', 'easymock\/test-deploy\/src\/main\/java\/',
                      'easymock\/test-integration\/src\/main\/java\/', 'easymock\/test-integration\/src\/test\/java\/',
                      'easymock\/test-java8\/src\/test\/java\/', 'easymock\/test-junit5\/src\/test\/java\/', 'easymock\/test-nodeps\/src\/test\/java\/',
                      'easymock\/test-osgi\/src\/test\/java\/', 'easymock\/test-testng\/src\/test\/java\/',
                      'easymock\/src\/test\/java\/', 'easymock\/src\/java\/', 'easymock\/src\/main\/java\/', 'easymock\/src\/test\/',
                      ''],
         'jgit': ['org.eclipse.jgit.ant.test\/tst\/', 'org.eclipse.jgit.ant.test\/src\/', 'org.eclipse.jgit.ant.test\/',
                  'org.eclipse.jgit.ant\/src\/',
                  'org.eclipse.jgit.ant\/', 'org.eclipse.jgit.archive\/src\/', 'org.eclipse.jgit.http.apache\/src\/',
                  'org.eclipse.jgit.http.server\/src\/', 'org.eclipse.jgit.http.server\/',
                  'org.eclipse.jgit.http.test\/tst\/', 'org.eclipse.jgit.http.test\/src\/',
                  'org.eclipse.jgit.http.test\/', 'org.eclipse.jgit.junit.http\/src\/', 'org.eclipse.jgit.junit\/src\/',
                  'org.eclipse.jgit.junit\/',
                  'org.eclipse.jgit.lfs.server.test\/tst\/', 'org.eclipse.jgit.lfs.server.test\/',
                  'org.eclipse.jgit.lfs.server\/src\/',
                  'org.eclipse.jgit.lfs.server\/', 'org.eclipse.jgit.lfs.test\/tst\/', 'org.eclipse.jgit.lfs.test\/src\/',
                  'org.eclipse.jgit.lfs.test\/',
                  'org.eclipse.jgit.lfs\/src\/', 'org.eclipse.jgit.lfs\/', 'org.eclipse.jgit.packaging\/',
                  'org.eclipse.jgit.pgm.test\/tst\/', 'org.eclipse.jgit.pgm.test\/src\/',
                  'org.eclipse.jgit.pgm\/src\/', 'org.eclipse.jgit.test\/tst\/', 'org.eclipse.jgit.test\/src\/',
                  'org.eclipse.jgit.test\/exttst', 'org.eclipse.jgit.test\/', 'org.eclipse.jgit.ui\/src\/',
                  'org.eclipse.jgit\/src\/', 'org.eclipse.jgit\/', 'org.eclipse.jgit.src\/', ''],

'Openfire': [
             'starter\/src\/main\/java\/', 'xmppserver\/src\/main\/java\/',
             'xmppserver\/src\/test\/throttletest\/src\/',
             'xmppserver\/src\/test\/java\/',
             'plugins\/tikitoken\/src\/java\/',
             'plugins\/sip\/src\/java\/',
             'plugins\/loadStats\/src\/java\/',
             'plugins\/nonSaslAuthentication\/src\/java\/',
             'plugins\/xmldebugger\/src\/java\/',
             'plugins\/mucservice\/src\/java\/',
             'plugins\/emailListener\/src\/java\/',
             'plugins\/inverse\/src\/java\/',
             'plugins\/userImportExport\/src\/test\/java\/',
             'plugins\/registration\/src\/java\/',
             'plugins\/justmarried\/src\/java\/',
             'plugins\/monitoring\/src\/java\/',
             'plugins\/clientControl\/src\/java\/',
             'plugins\/externalservicediscovery\/src\/test\/',
             'plugins\/dbaccess\/src\/java\/',
             'plugins\/restAPI\/src\/java\/',
             'plugins\/contentFilter\/src\/test\/java\/',
             'plugins\/hazelcast\/src\/java\/',
             'plugins\/candy\/src\/java\/',
             'plugins\/fastpath\/src\/java\/',
             'plugins\/certificateManager\/src\/java\/',
             'plugins\/httpFileUpload\/src\/java\/',
             'plugins\/subscription\/src\/java\/',
             'plugins\/packetFilter\/src\/java\/',
             'plugins\/presence\/src\/java\/',
             'plugins\/bookmarks\/src\/java\/',
             'plugins\/broadcast\/src\/java\/',
             'plugins\/userservice\/src\/java\/',
             'plugins\/motd\/src\/java\/',
             'plugins\/userCreation\/src\/java\/',
             'plugins\/gojara\/src\/java\/',
             'plugins\/stunserver\/src\/java\/',
             'plugins\/userStatus\/src\/java\/',
             'plugins\/search\/src\/java\/',
             'src\/java\/', 'src\/test\/java\/']
        }

def format_method(row):
    method_name = row['CLASS_PREVIOUSNAME']

    proj = row['PROJECT_NAME']
    for p in packs[proj]:
        pattern = r'\/project[AB]\/' + p
        name = re.split(pattern, method_name)
        if len(name) > 1:
            method_name = name[1]

    method_name = method_name.replace('.java', '')
    method_name = method_name.replace('/', '.')
    method_name = method_name.replace(' ', '')

    return method_name


def join_change_distiller(project_name, current_hash):
    # print("Change distiller")
    csv_path = '../5.cd/results/' + project_name + '-cd-methods-results.csv'

    metrics = ["PROJECT_NAME", "PREVIOUS_COMMIT", "CURRENT_COMMIT", "CLASS_CURRENTCOMMIT", "CLASS_PREVIOUSCOMMIT",
               "CLASS_CURRENTNAME", "CLASS_PREVIOUSNAME",
               "STATEMENT_DELETE", "STATEMENT_INSERT", "STATEMENT_ORDERING_CHANGE",
               "STATEMENT_PARENT_CHANGE", "STATEMENT_UPDATE", "TOTAL_STATEMENTLEVELCHANGES",
               "PARENT_CLASS_CHANGE", "PARENT_CLASS_DELETE", "PARENT_CLASS_INSERT", "CLASS_RENAMING",
               "TOTAL_CLASSDECLARATIONCHANGES",
               "RETURN_TYPE_CHANGE", "RETURN_TYPE_DELETE", "RETURN_TYPE_INSERT", "METHOD_RENAMING",
               "PARAMETER_DELETE", "PARAMETER_INSERT", "PARAMETER_ORDERING_CHANGE", "PARAMETER_RENAMING",
               "PARAMETER_TYPE_CHANGE", "TOTAL_METHODDECLARATIONSCHANGES",
               "ATTRIBUTE_RENAMING", "ATTRIBUTE_TYPE_CHANGE", "TOTAL_ATTRIBUTEDECLARATIONCHANGES",
               "ADDING_ATTRIBUTE_MODIFIABILITY", "REMOVING_ATTRIBUTE_MODIFIABILITY",
               "REMOVING_CLASS_DERIVABILITY", "REMOVING_METHOD_OVERRIDABILITY",
               "ADDING_CLASS_DERIVABILITY", "ADDING_CLASS_DERIVABILITY", "ADDING_METHOD_OVERRIDABILITY",
               "TOTAL_DECLARATIONPARTCHANGES", "TOTAL_CHANGES"]

    df = pd.read_csv(csv_path,  sep=',', engine='python', index_col=False)
    df.columns = metrics
    df = df[(df['CURRENT_COMMIT'] == current_hash)]

    if len(df.index):
        df['method_name'] = df.apply(format_method, axis=1)

    # print(df.shape[0])
    return df
