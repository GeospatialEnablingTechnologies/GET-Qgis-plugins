# -*- coding: utf-8 -*-
# Import the PyQt and QGIS libraries
from PyQt4 import QtCore, QtGui
from qgis import *
from qgis.core import *
import re
import resources


class Vertices_Counter:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        self.canvas = iface.mapCanvas()

    def initGui(self):
        self.menu = QtGui.QMenu(self.iface.pluginMenu())
        # Create action that will start plugin
        self.action = QtGui.QAction(QtGui.QIcon(":icons/verts.png"), "Vertices Counter", self.iface.pluginMenu())
        # connect the action to the run method
        QtCore.QObject.connect(self.action, QtCore.SIGNAL("activated()"), self.build_ui)
        
        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("Vertices Counter",self.action)
        


    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu("Vertices Counter",self.action)



    # run
    def build_ui(self):
        self.iface.currentLayerChanged.connect(self.curr_layer_changed)
        self.MapLayerRegistry=QgsMapLayerRegistry.instance()
        self.MapLayerRegistry.layerRemoved.connect(self.refresh_layers)
        self.MapLayerRegistry.layerWasAdded.connect(self.refresh_layers)
        
        
        self.width=420
        self.height=660
        window_dim=QtCore.QSize(self.width,self.height)
        s=QtGui.QDesktopWidget()
   
        window_size=QtCore.QRect(s.geometry())
        
        self.mainWind=QtGui.QMainWindow(self.iface.mainWindow())
        self.mainWind.resize(window_dim)
        self.mainWind.setWindowTitle("Vertices Counter")
        self.mainWind.setWindowIcon(QtGui.QIcon(":icons/verts.png"))
        self.mainWind.setLayoutDirection(QtCore.Qt.LayoutDirection(QtCore.Qt.RightSection))
        self.mainWind.setMaximumSize(window_dim)
        self.mainWind.setMinimumSize(window_dim)
        self.mainWind.move(window_size.width()*2/3,window_size.height()*1/5)
       
        self.tabwidget=QtGui.QTabWidget(self.mainWind)
        self.tabwidget.resize(window_dim)
        self.tabwidget.setAutoFillBackground(False)
        self.tabwidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabwidget.setUsesScrollButtons(False)
        self.tab1=QtGui.QWidget()
        
        self.widget=QtGui.QWidget(self.tab1)
        self.widget.resize(window_dim)
        self.group_layers_import=QtGui.QGroupBox(self.widget)
        self.group_layers_import.setGeometry(QtCore.QRect(10, 10, 400, 150))
        self.group_layers_import.setTitle("Layer Selection")
        #######################################################################
        ######### LAYOUT 0 ####################################################
        self.radio_active_layer=QtGui.QRadioButton(self.group_layers_import)
        self.radio_active_layer.setGeometry(QtCore.QRect(5, 20, 200, 20))
        
        self.radio_active_layer.clicked.connect(self.active_layer_mode)
        #######################################################################
        ######### LAYOUT 1 ####################################################
         
        self.radio_opened_layers=QtGui.QRadioButton(self.group_layers_import)
        self.radio_opened_layers.setGeometry(QtCore.QRect(5, 40, 200, 20))
        self.radio_opened_layers.setText("Select from loaded layers :")
        self.radio_opened_layers.clicked.connect(self.loaded_layers_mode)
       
        ########################################################################
        ######### LAYOUT 2 - Opened Layers - Select from Combo Box #############
        self.opened_layers_widget=QtGui.QWidget(self.group_layers_import)
        self.opened_layers_widget.setGeometry(25,60,self.width,20)
        self.label1 = QtGui.QLabel(self.opened_layers_widget)
        self.label1.setGeometry(QtCore.QRect(0, 0, 60, 20))
        self.label1.setText("Select Layer " )
         
         
        self.combo=QtGui.QComboBox(self.opened_layers_widget)
        self.combo.setGeometry(QtCore.QRect(70, 0, 150, 20))
        self.combo.currentIndexChanged.connect(self.check_check_vector_layer_type_for_list)
        
        self.refresh_button = QtGui.QPushButton(self.opened_layers_widget)
        self.refresh_button.setGeometry(QtCore.QRect(230, 0, 80, 20))
        self.refresh_button.setText("Refresh")
        self.refresh_button.clicked.connect(self.refresh_layers)
        
        #######################################################################
        ######### LAYOUT 3 ####################################################
        self.radio_openfile=QtGui.QRadioButton(self.group_layers_import)
        self.radio_openfile.setGeometry(QtCore.QRect(5, 85, 200, 20))
        self.radio_openfile.setText("Open layer from file :")
        self.radio_openfile.clicked.connect(self.open_file_mode)
        
        ########################################################################
        ######### LAYOUT 4 - Opened Layers - Select from Combo Box #############
        self.open_file_widget=QtGui.QWidget(self.group_layers_import)
        self.open_file_widget.setGeometry(25,110,self.width,20)
        self.label2 = QtGui.QLabel(self.open_file_widget)
        self.label2.setGeometry(QtCore.QRect(0, 0, 60, 20))
        self.label2.setText("Select file : " )
        
        self.text3 = QtGui.QLineEdit(self.open_file_widget)
        self.text3.setGeometry(QtCore.QRect(70, 0,220, 20))
        self.text3.setText("" )
         
        self.openfile_button = QtGui.QPushButton(self.open_file_widget)
        self.openfile_button.setGeometry(QtCore.QRect(300, 0, 30, 20))
        self.openfile_button.setText("...")
        self.openfile_button.clicked.connect(self.open_file_dialog)
        
        ########################################################################
        ######### LAYOUT 5 -Count options #############
        
        self.group_count_options=QtGui.QGroupBox(self.widget)
        self.group_count_options.setGeometry(QtCore.QRect(10, 170, self.width-20, 110))
        self.group_count_options.setTitle("Options")
        
        self.edit_options=QtGui.QWidget(self.group_count_options)
        
        self.radio_new_col=QtGui.QRadioButton(self.edit_options)
        self.radio_new_col.setGeometry(QtCore.QRect(10, 20, 130, 20))
        self.radio_new_col.setText("Create new column")
        self.radio_new_col.clicked.connect(self.add_col_mode)
        self.radio_new_col.setChecked(True)
        
        self.column_name=QtGui.QLineEdit(self.edit_options)
        self.column_name.setGeometry(QtCore.QRect(140, 20, 60, 20))
        self.column_name.setText("Vertices")
        self.column_name.setEnabled(True)
                
        
        self.check_drop=QtGui.QCheckBox(self.edit_options)
        self.check_drop.setGeometry(QtCore.QRect(30, 50, 130, 20))
        self.check_drop.setText("Drop existing one")
        self.check_drop.setChecked(True)
        
        self.radio_no_col=QtGui.QRadioButton(self.edit_options)
        self.radio_no_col.setGeometry(QtCore.QRect(10, 80, 170, 20))
        self.radio_no_col.setText("Count without adding a column")
        self.radio_no_col.clicked.connect(self.no_add_col_mode)
        
         
        line=QtGui.QFrame(self.group_count_options)
        line.setFrameShape(QtGui.QFrame.VLine)
        line.setFrameShadow(QtGui.QFrame.Sunken)
        line.setGeometry(210,20,20,80)
         
        
        self.check_count_selected=QtGui.QCheckBox(self.group_count_options)
        self.check_count_selected.setGeometry(QtCore.QRect(250, 20, 180, 40))
        self.check_count_selected.setText("Count Vertices for\nSelected Features")
         
        
        
        self.calc_all_button=QtGui.QPushButton(self.widget)
        self.calc_all_button.setGeometry(QtCore.QRect((self.width/2)-60,290, 120, 40))
        self.calc_all_button.setText("Count Vertices")
        self.calc_all_button.clicked.connect(self.start_cal)
        ########################################################################
        ######### LAYOUT 5 -Count buttons #############
        
        self.group_results=QtGui.QGroupBox(self.widget)
        self.group_results.setGeometry(QtCore.QRect(10,340,self.width-20,self.height-340-30))
        self.group_results.setTitle("Results")
        
        self.calc_widget=QtGui.QWidget(self.group_results)
        self.calc_widget.setGeometry(10,10,self.width-10,self.height-290-30)
        self.calc_widget.setEnabled(False)
         
        
        self.total_verts=QtGui.QLabel(self.calc_widget)
        self.total_verts.setGeometry(QtCore.QRect(250,10, 120, 40))
        self.total_verts.setAlignment(QtCore.Qt.AlignCenter)
        self.total_verts.setText("")
         
       
         
        
        
        
        
        self.add_to_map_button=QtGui.QPushButton(self.calc_widget)
        self.add_to_map_button.setGeometry(QtCore.QRect(250,self.height-340-30-50, 120, 20))
        self.add_to_map_button.setText("Add Vector on Map")
        self.add_to_map_button.clicked.connect(self.add_to_map)
       
        
        
        
        
        
        ########################################################################
        ######### LAYOUT 6 - Table #############
        
        self.table = QtGui.QTableWidget(self.calc_widget)
        self.table.setGeometry(QtCore.QRect(10, 10,204,self.calc_widget.height()-80))
        self.table.setSortingEnabled(True)
        
        self.table.setColumnCount(2)
         
        col1 = QtGui.QTableWidgetItem()
        col1.setText("Feature")
        self.table.setHorizontalHeaderItem(0, col1)
        col2 = QtGui.QTableWidgetItem()
        col2.setText("Vertices")
        self.table.setHorizontalHeaderItem(1, col2)
        self.table.verticalHeader().hide()
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)        
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table.itemClicked.connect(self.show_hide_feature)
        
       
        
   
        self.file_layer_current=False
        
        self.tabwidget.addTab(self.tab1,"Counter")
        
        
        self.tab2=QtGui.QWidget()
        self.centralWidget = QtGui.QWidget(self.tab2)
        self.centralWidget.setObjectName("centralWidget")
        self.centralWidget.resize(self.width,self.height)
        file_html=QtCore.QFile(':help.html')
        file_html.open(QtCore.QFile.ReadOnly|QtCore.QFile.Text)
        istream = QtCore.QTextStream(file_html)
        self.help_browser=QtGui.QTextBrowser(self.centralWidget)
        self.help_browser.setGeometry(QtCore.QRect(0,0,self.width,self.height))
        self.help_browser.setHtml(istream.readAll())
        self.help_browser.setOpenExternalLinks(True)
        
        
        self.tabwidget.addTab(self.tab2,"Help")
        
        self.tab3=QtGui.QWidget()
        self.centralWidget = QtGui.QWidget(self.tab3)
        self.centralWidget.setObjectName("centralWidget")
        self.centralWidget.resize(self.width,self.height)
        file_html=QtCore.QFile(':info.html')
        file_html.open(QtCore.QFile.ReadOnly|QtCore.QFile.Text)
        istream = QtCore.QTextStream(file_html)
        self.about_browser=QtGui.QLabel(self.centralWidget)
        self.about_browser.setGeometry(QtCore.QRect(10,10,420,500))
        
         
        self.about_browser.setText(istream.readAll())
        self.about_browser.setOpenExternalLinks(True)
        
        self.tabwidget.addTab(self.tab3,"About")
        
        
        self.mainWind.show()
        self.refresh_layers()
        self.radio_active_layer.click()
        self.curr_layer_changed() 
       
        return
    def curr_layer_changed(self):
        
        layer=self.iface.activeLayer()
       
        if not layer==None:
            self.radio_active_layer.setText("Active Layer : %s"%(layer.name()))
            if layer.type()==0:
                self.vector_mode()
                self.check_vector_layer_type(layer)
            else:
                self.not_vector_mode()
        else:
            self.radio_active_layer.setText("Active Layer : No layers loaded")
        
         
    
    def check_vector_layer_type(self,layer):
        
        data_type=str(layer.storageType())
        if not data_type=="ESRI Shapefile" :
            self.vector_mode()
            self.edit_options.setEnabled(False)
            self.no_options_avalaible()
        else:
            self.edit_options.setEnabled(True)
            self.options_avalaible()
        
    
    def check_check_vector_layer_type_for_list(self):
        item=self.combo.currentIndex()
        if item>=0 :
            layer=self.layers[item]
            if layer.type()==0:
                self.vector_mode()
                data_type=str(layer.storageType())
                if not data_type=="ESRI Shapefile" :
                    self.edit_options.setEnabled(False)
                    self.no_options_avalaible()
                else:
                    self.edit_options.setEnabled(True)
                    self.options_avalaible()
            else:
                self.not_vector_mode()
                
                
            
    def refresh_layers(self):   
         
        self.layers = self.iface.legendInterface().layers()
        layer_list=[]
        self.combo.clear()
        if self.iface.activeLayer()==None:
            if len(self.layers)==0:
                self.radio_active_layer.setText("Active Layer : No layers loaded")
            else:
                self.iface.setActiveLayer(self.layers[0])
        
        for lay in self.layers:
            
            layer_list.append(lay.name())
            
        self.combo.addItems(layer_list)
        
        if len(layer_list)==0:
            self.calc_widget.setEnabled(False)
        else:
            self.calc_widget.setEnabled(True)
    
    def active_layer_mode(self):
        self.refresh_layers()
        self.clear_table()
        self.mode='active'
        self.total_verts.setText("")
        self.opened_layers_widget.setEnabled(False)
        self.open_file_widget.setEnabled(False)
        self.check_count_selected.setEnabled(True)
        self.add_to_map_button.setVisible(False)
        self.add_to_map_button.setEnabled(False)

         
         
        layer=self.iface.activeLayer()
        if not len(self.layers)==0:
            self.radio_active_layer.setText("Active Layer : %s"%(layer.name()))
        
    
    def loaded_layers_mode(self):
        
        self.clear_table()
        self.mode='loaded_layers'
        self.total_verts.setText("")
        self.opened_layers_widget.setEnabled(True)
        self.open_file_widget.setEnabled(False)
        self.check_count_selected.setEnabled(True)
        self.add_to_map_button.setVisible(False)
        self.add_to_map_button.setEnabled(False)
      
        self.refresh_layers()
        
        
    def open_file_mode(self):
        self.refresh_layers()
        
        self.clear_table()
        self.mode='open_file'
        self.total_verts.setText("")
        self.opened_layers_widget.setEnabled(False)
        self.open_file_widget.setEnabled(True)
        self.check_count_selected.setEnabled(False)
        self.add_to_map_button.setVisible(True)
        if self.file_layer_current:
            self.add_to_map_button.setEnabled(True)
        else:
            self.add_to_map_button.setEnabled(False)
        
    def add_col_mode(self):
        self.check_drop.setEnabled(True)
        self.column_name.setEnabled(True)
        
    def no_add_col_mode(self):
        self.check_drop.setEnabled(False)
        self.column_name.setEnabled(False)
    
    def options_avalaible(self):
        self.radio_no_col.setChecked(False)
        self.radio_new_col.setChecked(True)
        self.check_drop.setChecked(True)
    
    def no_options_avalaible(self):
        self.radio_no_col.setChecked(True)
        self.radio_new_col.setChecked(False)
        self.check_drop.setChecked(False)
        
    def not_vector_mode(self):
        self.group_count_options.setEnabled(False)
        self.group_results.setEnabled(False)
        
        
    def vector_mode(self):
        self.group_count_options.setEnabled(True)
        self.group_results.setEnabled(True)
        
    
    def open_file_dialog(self):
        
        filename = QtGui.QFileDialog.getOpenFileName(self.mainWind, "Select Shapefile ","", "ESRI Shapefiles [OGR](*.shp *.SHP)")
       
        #drive,path_and_file=os.path.splitdrive(filename)
        #path,file=os.path.split(path_and_file)
        
        self.text3.setText(filename)
        
    def start_cal(self):
        self.clear_table()
        if self.check_count_selected.isChecked() and self.check_count_selected.isEnabled():
            self.do_calc_feat()
        else:
            self.do_calc()
             
    
    def do_calc(self):
        
        if self.radio_opened_layers.isChecked():
            item=self.combo.currentIndex()
            if item>=0 :
                layer=self.layers[item]
                if not layer.type()==0:
                    
                    self.calc_widget.setEnabled(False) 
                    errorbox=QtGui.QMessageBox(self.mainWind)
                    errorbox.setText("Please select a Vector Layer!")
                    errorbox.setWindowTitle("Invalid Layer !")
                    errorbox.show()
                else:
                    self.calc_widget.setEnabled(True)
                    self.layer=layer
                    self.edit_whole_layer(layer)
                    self.file_layer_current=False
            else:
                errorbox=QtGui.QMessageBox(self.mainWind)
                errorbox.setText("No Layers Loaded!")
                errorbox.setWindowTitle("Error !")
                errorbox.show()
                
        elif self.radio_active_layer.isChecked():
            layer=self.iface.activeLayer()
            if layer!=None:
                
                
                if not layer.type()==0:
                   
                    self.calc_widget.setEnabled(False) 
                    errorbox=QtGui.QMessageBox(self.mainWind)
                    errorbox.setText("Please select a Vector Layer!")
                    errorbox.setWindowTitle("Invalid Layer !")
                    errorbox.show()
                else:
                    self.layer=layer
                    self.calc_widget.setEnabled(True)
                    self.edit_whole_layer(layer)
                    self.file_layer_current=False
            else:
                errorbox=QtGui.QMessageBox(self.mainWind)
                errorbox.setText("No Layer Loaded!")
                errorbox.setWindowTitle("Error !")
                errorbox.show()
            
        elif self.radio_openfile.isChecked():
           
           
            filename=self.text3.text()
            path_parts=re.split(r'/', filename)
            fname=path_parts[len(path_parts)-1].split('.')
             
            layer = QgsVectorLayer(self.text3.text(), fname[0], "ogr")
            
            if not layer.isValid():
                self.calc_widget.setEnabled(False) 
                errorbox=QtGui.QMessageBox(self.mainWind)
                errorbox.setText("Invalid File !")
                errorbox.setWindowTitle("Error !")
                errorbox.show()
            else:
                self.file_layer_current=True
                self.flayer=layer
                self.calc_widget.setEnabled(True)
                self.add_to_map_button.setEnabled(True)
                self.edit_whole_layer(layer)
    
    def do_calc_feat(self):
       
        if self.radio_opened_layers.isChecked():
            item=self.combo.currentIndex()
            if item>=0:
                layer=self.layers[item]
                self.layer=layer
            else:
                layer=None
             
        elif self.radio_active_layer.isChecked():
            layer=self.iface.activeLayer()
            self.layer=layer
            
         
        
        if not layer==None:    
            if not layer.type()==0:
                   
                self.calc_widget.setEnabled(False) 
                errorbox=QtGui.QMessageBox(self.mainWind)
                errorbox.setText("Please select a Vector Layer!")
                errorbox.setWindowTitle("Invalid Layer !")
                errorbox.show()
            else:
                if len(layer.selectedFeatures())>0:  
                    self.calc_widget.setEnabled(True)
                    self.edit_layer_feat(layer)
                    self.file_layer_current=False
            
                else:
                    errorbox=QtGui.QMessageBox(self.mainWind)
                    errorbox.setText("No features selected !")
                    errorbox.setWindowTitle("Error !")
                    errorbox.show()
        else:
                errorbox=QtGui.QMessageBox(self.mainWind)
                errorbox.setText("No Layer Loaded!")
                errorbox.setWindowTitle("Error !")
                errorbox.show()
            
            
            
            
     
        

        
    
    def edit_whole_layer(self,layer):
        
        self.table.clearContents()

        if self.radio_new_col.isEnabled() and self.radio_new_col.isChecked():
            layer.startEditing()
        fields= layer.dataProvider().fields()
        i=0
        if self.check_drop.isChecked():
            for curr_field in fields:
                if curr_field.name()==self.column_name.text():
                    ints=[]
                    ints.append(i)
               
                    layer.dataProvider().deleteAttributes(ints)
                i=i+1
        
        layer.dataProvider().addAttributes( [ QgsField(self.column_name.text(), QtCore.QVariant.Int) ] )
        provider = layer.dataProvider()
        vertices_field_index = provider.fieldNameIndex(self.column_name.text())
       
        s=provider.getFeatures()
        
        feat = QgsFeature()
        vertex_count = 0
        attribute_dict = {}
        row=0
        while s.nextFeature(feat):
            layer_vertices = 0
            self.table.setRowCount(row+1)
            geom = feat.geometry()
            if geom.type() == QGis.Polygon:
               
                if geom.isMultipart():
                    polygons = geom.asMultiPolygon()
                else:
                    polygons = [ geom.asPolygon() ]
                for polygon in polygons:
                    for ring in polygon:
                        layer_vertices += len(ring)
                
                 
            if geom.type() == QGis.Line:
                 
                if geom.isMultipart():
                    lines = geom.asMultiPolyline()
                else:
                    lines = [ geom.asPolyline() ]
                    
                for line in lines:
                    layer_vertices += len(line)
                 
                 
            if geom.type() == QGis.Point:
                 
                if geom.isMultipart():
                    points = geom.asMultiPoint()
                else:
                    points = [ geom.asPoint() ]
                for point in points:
                    layer_vertices += 1
             
                    
                
            self.add_item(row,feat.id(),layer_vertices)
            vertex_count += layer_vertices
            attribute_dict[feat.id()] = { vertices_field_index: str(layer_vertices) }
            row+=1
       
        self.show_total(vertex_count)
        
        if self.radio_new_col.isChecked():
            layer.dataProvider().changeAttributeValues(attribute_dict)
            layer.commitChanges()
    
    def edit_layer_feat(self,layer):
        
        self.table.clearContents()
        
        layer.startEditing()
        fields= layer.dataProvider().fields()
        i=0
        if self.radio_new_col.isEnabled() and self.radio_new_col.isChecked():
            for curr_field in fields:
                if curr_field.name()==self.column_name.text():
                    ints=[]
                    ints.append(i)
               
                    layer.dataProvider().deleteAttributes(ints)
                i=i+1
        
        layer.dataProvider().addAttributes( [ QgsField(self.column_name.text(), QtCore.QVariant.Int) ] )
        provider = layer.dataProvider()
        vertices_field_index = provider.fieldNameIndex(self.column_name.text())
        
        feats = layer.selectedFeatures()
        self.table.setRowCount(len(feats))
        vertex_count = 0
        attribute_dict = {}
        row=0
        for feat in feats:
            layer_vertices = 0
            geom = feat.geometry()
            if geom.type() == QGis.Polygon:
                
                if geom.isMultipart():
                    polygons = geom.asMultiPolygon()
                else:
                    polygons = [ geom.asPolygon() ]
                for polygon in polygons:
                    for ring in polygon:
                        layer_vertices += len(ring)
                
                 
            elif geom.type() == QGis.Line:
                 
                if geom.isMultipart():
                    lines = geom.asMultiPolyline()
                else:
                    lines = [ geom.asPolyline() ]
                    
                for line in lines:
                    layer_vertices += len(line)
                 
                 
            elif geom.type() == QGis.Point:
                 
                if geom.isMultipart():
                    points = geom.asMultiPoint()
                else:
                    points = [ geom.asPoint() ]
                for point in points:
                    layer_vertices += 1
            
                
                 
                
            self.add_item(row,feat.id(),layer_vertices)
            vertex_count += layer_vertices
            attribute_dict[feat.id()] = { vertices_field_index: str(layer_vertices) }
            row+=1
       
        self.show_total(vertex_count)
       
        if self.radio_new_col.isChecked():
            layer.dataProvider().changeAttributeValues(attribute_dict)
            layer.commitChanges()
    
    def add_item(self,row,featid,vert):
        item1 = QtGui.QTableWidgetItem()
        item1.setData(QtCore.Qt.DisplayRole,featid)
        self.table.setItem(row,0,item1)
        item2 = QtGui.QTableWidgetItem()
        item2.setData(QtCore.Qt.DisplayRole,vert)
        self.table.setItem(row,1,item2)
        
    def show_hide_feature(self):
        if self.mode=='active':
             
            row=self.table.currentRow()
            item=self.table.item(row,0)
            data=item.data(0)
       
            selected=False
            for feat in self.layer.selectedFeatures():
                if data==feat.id():
                    selected=True
            if selected:
                self.layer.deselect(data)
            else:
                self.layer.select(data)
           
    def show_total(self,count):
        self.total_verts.setText("Total Vertices : "+str(count))
    def hide_feats(self):
        sel=self.layer.selectedFeatures()
        for selected in sel:
            self.layer.deselect(selected.id())
    def add_to_map(self):
        self.MapLayerRegistry.addMapLayer(self.flayer)
    
    def clear_table(self):
        self.table.clearContents()
        self.table.setRowCount(0);
    


if __name__ == "__main__":
    pass
