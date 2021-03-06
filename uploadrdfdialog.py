
from qgis.PyQt.QtWidgets import QDialog, QLabel, QLineEdit,QPushButton,QCheckBox,QListWidget,QComboBox,QMessageBox,QRadioButton,QListWidgetItem,QTableWidgetItem,QTableWidget,QPlainTextEdit
from qgis.core import QgsProject
from qgis.PyQt import uic
from rdflib import Graph, Literal, URIRef
from rdflib.plugins.stores import sparqlstore
from .searchdialog import SearchDialog
from .sparqlhighlighter import SPARQLHighlighter
from SPARQLWrapper import SPARQLWrapper, JSON
import json
import requests
import os.path

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'uploadrdfdialog.ui'))
## Dialog to upload a generated RDF result to a triple store.
class UploadRDFDialog(QDialog,FORM_CLASS):
	
    currentrow=""
	
    triplestoreconf=""
	
    interlinkOrEnrich=False
    
    searchResultMap={}

    table=False
    
    valmaptable=False
	
    fieldname=""

    def __init__(self,ttlstring):
        super(QDialog, self).__init__()
        self.setupUi(self)
        self.ttlstring=ttlstring   
        self.checkConnectionButton.clicked.connect(self.checkConnection)  
        self.applyButton.clicked.connect(self.uploadResult)

    ## 
    #  @brief Checks the connection to a triple store which has been defined by a given internet address.
    #  
    #  @param self The object pointer
    #  @return True if the connection was successful, false otherwise 
    def checkConnection(self):
        print("")

		
    def compareLayers(layer1,layer2,idcolumn):
        changedTriples=""
        fieldnames = [field.name() for field in layer.fields()]
        for f in layer1.getFeatures():
            geom = f.geometry()
            id=f[idcolumn]
            expr = QgsExpression( "\""+idcolumn+"\"="+id )
            it = cLayer.getFeatures( QgsFeatureRequest( expr ) )
            #if len(it)==0:
                #Add new line
            #elif len(it)>0:
                #Compare

    ## Adds a new QGIS layer to a triplestore with a given address.
    #  @param self The object pointer.
    #  @param triplestoreaddress The address of the triple store
    #  @param layer The layer to add
    def addNewLayerToTripleStore(self,triplestoreaddress,layer):
        ttlstring=self.layerToTTLString(layer)
        queryString = "INSERT DATA { GRAPH <http://example.com/> { "+ttlstring+" } }" 
        sparql = SPARQLWrapper(triplestoreaddress)
        sparql.setQuery(queryString) 
        sparql.method = 'POST'
        sparql.query()

    def uploadResult(self):
        query_endpoint = 'http://localhost:3030/ds/query'
        update_endpoint = self.tripleStoreURL
        g=Graph()
        g.parse(data=self.ttlstring, format="ttl")
        store = sparqlstore.SPARQLUpdateStore()
        store.open((query_endpoint, update_endpoint))
        store.add_graph(g)
        self.close()
