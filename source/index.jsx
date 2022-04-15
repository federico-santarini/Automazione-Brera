var myDocument = app.documents.item(0);
var objectStyles = app.activeDocument.objectStyles;
for (p=0; p<myDocument.pages.length; p++) {
    var pageItems = app.activeDocument.pages[p].allPageItems
    var page = p+1
    for (i = pageItems.length- 1; i >= 0; i--) {
        var pageItem = pageItems[i];

        if (pageItem.appliedObjectStyle.name === 'Sinistra' && page%2 === 1) {
            pageItem.remove();
        } else if (pageItem.appliedObjectStyle.name === 'Destra' && page%2 === 0){
            pageItem.remove();
        }


    }
    
    
}