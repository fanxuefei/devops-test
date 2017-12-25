from xml.etree.ElementTree import ElementTree,Element
# import xml.etree.ElementTree as ET
import operator
class treeModel(object):
    def __init__(self,path):
        self.root = ''
        self.tree = ElementTree()
        self.parents = ''
        self.childrens = ''
        self.node = ''
        self.xmlpath = path
        self.readxml()
        self.is_Ture = False
        self.root_child = None
    def readxml(self):
        self.tree.parse(self.xmlpath)
        self.parents = self.tree.findall('network-lists/list')
    def is_find_cidr(self):
        for child in self.parents:
            if operator.eq(child.attrib['name'],'domains'):
                self.root_child = child
                for childname_node in  child :
                    if  'cidr' in  childname_node.attrib and operator.eq(childname_node.attrib['cidr'],'127.0.0.1'):
                        print(childname_node.attrib)
                        self.is_Ture = True
                        break
    def update_xml(self):
        self.is_find_cidr()
        if self.is_Ture:
            print('-------uuu------')
        else:
            print(self.root_child)
            print('-----mmm---------')
        # if is_Ture == False:
        #     '''
        #    这里开始新建一个cidr
        #
        #     '''
        #
        #

            # for childname in child.findall("allow"):
            #     if operator.eq(childname.attrib['name'],'domains'):
            #         for  in childname:
            #             if childname_node.attrib.has_key('cidr'):
            #                 print(childname_node.attrib)

if __name__ == '__main__':
    vc = treeModel("aaa.xml")
    vc.update_xml()

