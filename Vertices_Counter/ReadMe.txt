Description
Vertices Counter is a plugin that can be used for counting the vertices of simple and multi-part geometries. 

Usage notes

--Layer Selection:
1)	Active Layer Mode:
	In Active Layer Mode, vertices of the currently active layer are counted. User can choose between counting the vertices of the whole layer or just of the selected features. 
	While in this mode, user can also highlight features of his selection on the map, just by selecting the relevant row at the results grid.
2)	Loaded Layers Mode:
	In Loaded Layers Mode, user can count the vertices of one of the layers currently loaded in QGIS. Again, user can choose between counting the vertices of the whole layer or just of the selected features.
3)	Open Layer from File Mode:
	In Open Layer from File Mode, user can load a Shapefile and count vertices of the features contained. After specifying the path of the Shapefile and pressing Count Vertices the user can also (optionally) add the loaded layer on the map canvas.
--Options:
	=>	Create new column:
		User can choose this option, if he wants to add a new column at the Attribute Table of the layer, containing the results of the count.
	=>	Drop existing one:
		If this option is checked, any existing column already named as the column name inserted previously, will be overwritten.
	=>	Count without adding a new column:
		Choose this option, if you just want to perform the vertices� count and see the results without adding a new column at the Attribute Table.
Important Note 1:
This version of the plugin does not support adding a new column, containing the counting results, at the attribute table of layers loaded from databases.  
	=>	Count Vertices for Selected Features:
		Check this option when you want to count vertices only of the selected features.
--Results:
	This area contains the results in tabular format. First column contains the feature id as displayed in QGIS Attribute Table and the second one contains number of vertices per feature.
Important Note 2:
When performing count on polygon features, the plugin returns the total number of vertices in the geometry sense. E.g. for a rectangle it returns 5 as the number of vertices

Future Developments
* Writing count results at the attribute table of layers loaded from databases.
