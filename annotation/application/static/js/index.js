Vue.config.debug = true;
Vue.filter("highlight", function(text, query){
    var queries = query.split(" ");
    queries.forEach(function(q){
        var q = q.trim();
        if(q != ""){
            var matcher = new RegExp(q, "ig")
            text = text.toString().replace(matcher, function(matchedTxt, a, b){
                return ("<span class=\'highlight\'>" + matchedTxt + "</span>");
            });    
        }
    })
    return text;
});
var app = new Vue({
    el: "#app",
    delimiters: ["[[", "]]"],
    data: {
        selectedItemId: "",
        labels: {},
        task: {},
        _selectedTargetId: "",
        _selectionChanged: false,
        updated: false,
        documents: [],
        matchQuery: "",
        doneFilter: false
    },
    created: function(){
        var self = this;
        fetch("/documents", {credentials: "include"}).then(function(r){
            return r.json()
        }).then(function(json){
            self.documents = json["documents"]
        })
    },
    updated: function(){
        if(this._selectionChanged){
            document.getElementById("text-area").scrollTop = 0;
            this._selectionChanged = false;            
        }
    },
    computed:{
        selectedDocuments: function(){
            if(this.doneFilter){
                return this.documents.filter(function(d){ return d.done });
            }else{
                return this.documents;
            }
        },
        totalCount: function(){
            return this.documents.length;
        },
        doneCount: function(){
            var count = 0;
            this.documents.forEach(function(d){
                count += (d.done ? 1 : 0);
            })
            return count
        }        
    },
    methods: {
        selectItem: function(item_id){
            this._selectionChanged = true;
            if(item_id != this.selectedItemId && this.selectedItemId != "" && this.updated){
                var self = this;                
                self.saveAnnotation().then(function(){
                    self.fetchItem(item_id);
                })
            }else{
                this.fetchItem(item_id);
            }
        },
        itemClass: function(itemId){
            if(this.selectedItemId && this.selectedItemId == itemId){
                return ["item", "item-active"];
            }else{
                return ["item"];
            }
        },
        fetchItem: function(item_id){
            var self = this;
            var url = "/document/{}".replace("{}", item_id)
            return fetch(url, {credentials: "include"}).then(function(r){
                return r.json()
            }).then(function(json){
                self.selectedItemId = item_id
                self.updated = false;
                self.task = json;
                self.setLabels(json.labels)
                self.task.labels = [];
                self.task.labels = null;
            })
        },
        setLabels: function(labels){
            this.labels = {};
            for(var i = 0; i < labels.length; i++){
                var label = labels[i];
                if(!(label.label_group in this.labels)){
                    this.labels[label.label_group] = [];
                }
                this.labels[label.label_group].push(label);
            }
        },
        annotate: function(event){
            $el = event.target;
            this.updated = true;
            var labelId = $el.dataset.labelid;
            var selectedText = "";
            var selection = null;
            if(window.getSelection) {
                selection = window.getSelection()
                selectedText = selection.toString();
            } else if (document.selection && document.selection.type != "Control") {
                selection = document.selection
                selectedText = selection.createRange().text;
            }
            if(selectedText != "" && this._selectedTargetId != ""){
                var target = this.task.tasks[this._selectedTargetId];
                var positions = [selection.anchorOffset, selection.focusOffset];
                var position = [Math.min.apply(0, positions), Math.max.apply(0, positions)];
                var bodyText = selection.anchorNode.parentElement.textContent;
                var parentText = "";
                if(selection.anchorNode.parentElement.className == "highlight"){
                    //in highlighted 
                    parentText = selection.anchorNode.parentElement.parentElement.textContent;
                    var offset = parentText.indexOf(bodyText);
                    position = position.map(function(p){ return p + offset;});
                    bodyText = parentText;
                }else if (selection.anchorNode.previousElementSibling != null 
                          && selection.anchorNode.previousElementSibling.className == "highlight"){
                    // after highlighted
                    var offset = bodyText.indexOf(selection.anchorNode.textContent);
                    position = position.map(function(p){ return p + offset;});
                }    
                if(target.target != bodyText){
                    throw "Targeted Text is different.";
                }else if(selectedText != target.target.substring(position[0], position[1])){
                    throw "Position And Selected Text don't match.";
                }
                target.annotations.push({
                    "target_id": this._selectedTargetId,
                    "target": target.target,
                    "label": labelId,
                    "label_target": selectedText,
                    "position": position
                })
                target.annotations.sort(function(left, right){
                    return left.position[0] > right.position[0] ? 1 : -1;
                })
            }
        },
        saveAnnotation: function(){
            if(this.selectedItemId == ""){
                return;
            }
            
            var annotations = [];
            for(var target_id in this.task.tasks){
                var task = this.task.tasks[target_id];
                task.annotations.forEach(function(a){
                    annotations.push(a);
                })
            }
            var payload = {
                "annotations": annotations
            }
            var headers = new Headers({"Content-Type":"application/json"})
            payload = JSON.stringify(payload);
            var self = this;
            var url = "/document/{}".replace("{}", this.selectedItemId);
            return fetch(url, {method: "POST", headers: headers, body: payload, credentials: "include"}).then(function(r){
                self.updated = false;
                var edited = self.getDocument(self.selectedItemId);
                if(edited != null){
                    edited.done = true;
                }
                return r.json()
            })
        },
        getDocument: function(documentId){
            var result = null;
            this.documents.forEach(function(d){
                if(d.edi_id == documentId){
                    result = d;
                }
            })
            return result
        },
        setTarget: function(target_id){
            this._selectedTargetId = target_id
        },
        getAnnotationLabelStyle: function(annotation){
            var style = "";
            var label = annotation.label;
            for(var g in this.labels){
                for(var i = 0; i < this.labels[g].length; i++){
                    if(label == this.labels[g][i].label){
                        style = this.labels[g][i].display_style;
                    }
                }
            }
            return style
        },
        deleteAnnotation: function(target_id, annotation){
            var position = this.task.tasks[target_id].annotations.indexOf(annotation)
            this.task.tasks[target_id].annotations.splice(position, 1)
            this.updated = true;
        }
    }
})

// Key binds
document.addEventListener("DOMContentLoaded", function() {
    document.addEventListener("keydown", function(event){
        if (event.ctrlKey || event.metaKey) {
            switch (String.fromCharCode(event.which).toLowerCase()) {
                case "s":
                    event.preventDefault();
                    app.saveAnnotation()
                    break;
            }
            switch(event.which){
                case 39: //->
                    event.preventDefault();
                    var buttons = document.querySelectorAll("a[data-groupid='0']");
                    if(buttons.length > 0){
                        buttons[0].focus();
                    }
                    break;
            }
            if(event.shiftKey){
                var selected = app.selectedItemId;
                if(!selected){
                    return
                }
                var el = document.getElementById(selected);
                switch(event.which){
                    case 38: //↑
                        el.previousElementSibling.click();
                        break;
                        break;
                    case 40: //↓
                        el.nextElementSibling.click();
                        break;
                }
            }
        }
    });
});
