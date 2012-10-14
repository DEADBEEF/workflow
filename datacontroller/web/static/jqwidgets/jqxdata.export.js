/*
jQWidgets v2.4.2 (2012-Sep-12)
Copyright (c) 2011-2012 jQWidgets.
License: http://jqwidgets.com/license/
*/

(function(b){var a=(function(){var m={},j,k,r,g,d;function i(s){s.beginFile();f(s);o(s);s.endFile();return s.getFile()}function f(v){var t=true;b.each(k,function(){if(this.hidden){t=false;return false}});v.beginHeader(t);for(var s in k){var u=c(s,k[s]);v.appendHeaderCell(k[s],s,u,t)}v.endHeader(t)}function o(t){t.beginBody();for(var s=0;s<j.length;s+=1){q(t,j[s],s)}t.endBody()}function q(v,u,w){var t;v.beginRow();for(var s in k){t=n(w,s);if(u.hasOwnProperty(s)){v.appendBodyCell(u[s],k[s],t)}else{v.appendBodyCell("",k[s],t)}}v.endRow()}function c(t,u){if(u.style){return r[u.style]}var s=p();if(s.length>0){return s[0].style}return null}function p(){if(!d){d=new Array();b.each(r,function(s,t){d[d.length]={name:s,style:t}})}return d}function n(w,v){if(k[v]){if(k[v].cellStyle){var x=k[v];if(k[v].cellAltStyle){var t=w%2;if(t==0){return r[x.cellStyle]}return r[x.cellAltStyle]}return r[x.cellStyle]}else{var s=p();if(s.length>0){var t=w%(s.length-1);var u=s[t+1].style;return u}}}return null}function e(v,t,u){var s=document.createElement("input");s.name=t;s.value=v;s.type="hidden";u.appendChild(s);return s}function h(u,s,t){var v=document.createElement("textarea");v.name=s;v.value=u;v.type="hidden";t.appendChild(v);return v}function l(t,w,v,s){var u=document.createElement("form");e(t,"filename",u);e(w,"format",u);h(v,"content",u);if(s==undefined||s==""){s="http://www.jqwidgets.com/export_server/save-file.php"}u.action=s;u.method="post";document.body.appendChild(u);return u}g=function(v,u,t,s){if(!(this instanceof a)){return new a(v,u,t)}j=v;k=u;r=t;this.exportTo=function(x){x=x.toString().toLowerCase();var w=m[x];if(typeof w==="undefined"){throw"You can't export to "+x+" format."}return i(w,j,k,r)};this.exportToFile=function(z,w){var y=this.exportTo(z),x=l(w,z,y,s);x.submit();document.body.removeChild(x)};this.exportToLocalFile=function(y,w){var x=this.exportTo(y);document.location.href="data:application/octet-stream;filename="+w+","+encodeURIComponent(x)}};g.extend=function(s,t){if(t instanceof b.jqx.dataAdapter.DataExportModuleBase){m[s]=t}else{throw"The module "+s+" is not instance of DataExportModuleBase."}};return g}());b.jqx.dataAdapter.ArrayExporter=a})(jQuery);(function(b){var a=function(){this.formatData=function(f,e,c){if(e==="date"){var d="";if(typeof f==="string"){d=b.jqx.dataFormat.tryparsedate(f);f=d}if(f===""||f==null){return""}d=b.jqx.dataFormat.formatdate(f,c);if(d.toString()=="NaN"||d==null){return""}f=d}else{if(e==="number"){if(f===""||f==null){return""}var g=b.jqx.dataFormat.formatnumber(f,c);if(g.toString()=="NaN"){return""}else{f=g}}else{f=f}}if(f==null){return""}return f};this.getFormat=function(e){var c=e?e.formatString:"";var d="string";d=e?e.type:"string";if(d=="number"){if(!c){c="n2"}}if(d=="date"){if(!c){c="d"}}return{type:d,formatString:c}};this.beginFile=function(){throw"Not implemented!"};this.beginHeader=function(){throw"Not implemented!"};this.appendHeaderCell=function(){throw"Not implemented!"};this.endHeader=function(){throw"Not implemented!"};this.beginBody=function(){throw"Not implemented!"};this.beginRow=function(){throw"Not implemented!"};this.appendBodyCell=function(){throw"Not implemented!"};this.endRow=function(){throw"Not implemented!"};this.endBody=function(){throw"Not implemented!"};this.endFile=function(){throw"Not implemented!"};this.getFile=function(){throw"Not implemented!"}};b.jqx.dataAdapter.DataExportModuleBase=a})(jQuery);(function(d){var c=function(j){var e,h,g;var l=0;var i=this;this.beginFile=function(){e=""};this.beginHeader=function(){};this.appendHeaderCell=function(o,p,n,m){g=m;if(m){k(o.text)}};this.endHeader=function(){this.endRow()};this.beginBody=function(){l=0};this.beginRow=function(){if((l>0)||(l==0&&g)){e+="\n"}l++};this.appendBodyCell=function(n,m){k(n,m)};this.endRow=function(){e=e.substring(0,e.length-1)};this.endBody=function(){};this.endFile=function(){};this.getFile=function(){return e};function f(m,o){if(o){var n=i.getFormat(o);m=i.formatData(m,n.type,n.formatString)}if(m.toString().indexOf(h)>=0){m='"'+m+'"'}return m}function k(m,n){m=f(m,n);e+=m+j}};c.prototype=new d.jqx.dataAdapter.DataExportModuleBase();var a=function(){};a.prototype=new c(",");var b=function(){};b.prototype=new c("\t");d.jqx.dataAdapter.ArrayExporter.extend("csv",new a());d.jqx.dataAdapter.ArrayExporter.extend("tsv",new b())})(jQuery);(function(b){var a=function(){var d;var e;var f=0;this.beginFile=function(){d='<html>\n\t<head>\n\t\t<title></title>\n\t\t<meta http-equiv=Content-type content="text/html; charset=UTF-8">\n\t</head>\n\t<body>\n\t\t<table style="empty-cells: show;" cellspacing="0" cellpadding="2">'};this.beginHeader=function(){d+="\n\t\t\t<thead>"};this.appendHeaderCell=function(i,j,h,g){e=g;if(!g){return}if(i.width){d+='\n\t\t\t\t<th style="width: '+i.width+"px; "+c(h)+'">'+i.text+"</th>"}else{d+='\n\t\t\t\t<th style="'+c(h)+'">'+i.text+"</th>"}};this.endHeader=function(){d+="\n\t\t\t</thead>"};this.beginBody=function(){d+="\n\t\t\t<tbody>";f=0};this.beginRow=function(){d+="\n\t\t\t\t<tr>";f++};this.appendBodyCell=function(h,j,g){var i=this.getFormat(j);if(h===""){h="&nbsp;"}if(f==1&&!e){d+='\n\t\t\t\t\t<td style="'+c(g)+' border-top-width: 1px;">'+this.formatData(h,i.type,i.formatString)+"</td>"}else{d+='\n\t\t\t\t\t<td style="'+c(g)+'">'+this.formatData(h,i.type,i.formatString)+"</td>"}};this.endRow=function(){d+="\n\t\t\t\t</tr>"};this.endBody=function(){d+="\n\t\t\t</tbody>"};this.endFile=function(){d+="\n\t\t</table>\n\t</body>\n</html>\n"};this.getFile=function(){return d};function c(i){var g="";for(var h in i){if(i.hasOwnProperty(h)){g+=h+":"+i[h]+";"}}return g}};a.prototype=new b.jqx.dataAdapter.DataExportModuleBase();b.jqx.dataAdapter.ArrayExporter.extend("html",new a())})(jQuery);(function(b){var a=function(){var h,l,d,i,c,j,m={style:"",stylesMap:{font:{color:"Color","font-family":"FontName","font-style":"Italic","font-weight":"Bold"},interior:{"background-color":"Color",background:"Color"},alignment:{left:"Left",center:"Center",right:"Right"}},startStyle:function(p){this.style+='\n\t\t<ss:Style ss:ID="'+p+'" ss:Name="'+p+'">'},buildAlignment:function(q){if(q["text-align"]){var r=this.stylesMap.alignment[q["text-align"]];var p='\n\t\t\t<ss:Alignment ss:Vertical="Bottom" ss:Horizontal="'+r+'"/>';this.style+=p}},buildBorder:function(s){if(s["border-color"]){var r="\n\t\t\t<ss:Borders>";var u='\n\t\t\t\t<Border ss:Position="Bottom" ss:LineStyle="Continuous" ss:Weight="1" ss:Color="'+s["border-color"]+'"/>';var p='\n\t\t\t\t<Border ss:Position="Left" ss:LineStyle="Continuous" ss:Weight="1" ss:Color="'+s["border-color"]+'"/>';var q='\n\t\t\t\t<Border ss:Position="Right" ss:LineStyle="Continuous" ss:Weight="1" ss:Color="'+s["border-color"]+'"/>';var t='\n\t\t\t\t<Border ss:Position="Top" ss:LineStyle="Continuous" ss:Weight="1" ss:Color="'+s["border-color"]+'"/>';r+=u;r+=p;r+=q;r+=t;r+="\n\t\t\t</ss:Borders>";this.style+=r}},buildFont:function(q){var r=this.stylesMap.font,p="\n\t\t\t<ss:Font ";for(var s in r){if(typeof q[s]!=="undefined"){if(s==="font-style"&&q[s].toString().toLowerCase()==="italic"){p+='ss:Italic="1" '}else{if(s==="font-weight"&&q[s].toString().toLowerCase()==="bold"){p+='ss:Bold="1" '}else{if(s==="color"){p+="ss:"+r[s]+'="'+q[s]+'" '}}}}}p+="/>";this.style+=p},buildInterior:function(q){var r=this.stylesMap.interior,t="\n\t\t\t<ss:Interior ";var p=false;for(var s in r){if(typeof q[s]!=="undefined"){t+="ss:"+r[s]+'="'+q[s]+'" ';p=true}}if(p){t+='ss:Pattern="Solid"'}t+="/>";this.style+=t},buildFormat:function(q){if(q.dataType=="number"){var p=q.formatString;if(p==""||p.indexOf("n")!=-1){this.style+='\n\t\t\t<ss:NumberFormat ss:Format="#,##0.00_);[Red](#,##0.00)"/>'}else{if(p.indexOf("p")!=-1){this.style+='\n\t\t\t<ss:NumberFormat ss:Format="Percent"/>'}else{if(p.indexOf("c")!=-1){this.style+='\n\t\t\t<ss:NumberFormat ss:Format="Currency"/>'}}}}else{if(q.dataType=="date"){this.style+='\n\t\t\t<ss:NumberFormat ss:Format="Short Date"/>'}}},closeStyle:function(){this.style+="\n\t\t</ss:Style>"},toString:function(){var p=this.style;this.style="";return p}};this.beginFile=function(){c={};j=0;h='<?xml version="1.0"?>\n\t<?mso-application progid="Excel.Sheet"?> \n\t<Workbook xmlns="urn:schemas-microsoft-com:office:spreadsheet" \n\txmlns:o="urn:schemas-microsoft-com:office:office" \n\txmlns:x="urn:schemas-microsoft-com:office:excel" \n\txmlns:ss="urn:schemas-microsoft-com:office:spreadsheet" \n\txmlns:html="http://www.w3.org/TR/REC-html40"> \n\t<DocumentProperties xmlns="urn:schemas-microsoft-com:office:office"> \n\t<Version>12.00</Version> \n\t</DocumentProperties> \n\t<ExcelWorkbook xmlns="urn:schemas-microsoft-com:office:excel"> \n\t<WindowHeight>8130</WindowHeight> \n\t<WindowWidth>15135</WindowWidth> \n\t<WindowTopX>120</WindowTopX> \n\t<WindowTopY>45</WindowTopY> \n\t<ProtectStructure>False</ProtectStructure> \n\t<ProtectWindows>False</ProtectWindows> \n\t</ExcelWorkbook> \n\t<ss:Styles>'};this.beginHeader=function(){l='\n\t<ss:Worksheet ss:Name="Sheet1">\n\t\t<ss:Table>';d=[];i=[]};this.appendHeaderCell=function(r,s,q){var p=r.width!=undefined?r.width:r.text.length*10;l+='\n\t\t\t<ss:Column ss:Width="'+p+'"/>';d.push(r);i.push(q)};this.endHeader=function(p){if(p){this.beginRow();for(var q=0;q<d.length;q+=1){g.call(this,d[q]["text"],null,i[q])}this.endRow()}};this.beginBody=function(){};this.beginRow=function(){l+="\n\t\t\t<ss:Row>"};this.appendBodyCell=function(r,p,q){g.call(this,r,p,q)};this.endRow=function(){l+="\n\t\t\t</ss:Row>"};this.endBody=function(){l+="\n\t\t</ss:Table>"};this.endFile=function(){l+="\n\t</ss:Worksheet>\n</ss:Workbook>";h+="\n\t</ss:Styles>"};this.getFile=function(){return h+l};function g(s,u,r){var q="String";var t=this.getFormat(u);s=this.formatData(s,t.type,t.formatString);var p=f(r);l+='\n\t\t\t\t<ss:Cell ss:StyleID="'+p+'"><ss:Data ss:Type="'+q+'">'+s+"</ss:Data></ss:Cell>"}function n(){j+=1;return"xls-style-"+j}function k(q){for(var p in c){if(o(q,c[p])&&o(c[p],q)){return p}}return undefined}function o(t,q){var s=true;for(var r in t){if(t[r]!==q[r]){s=false}}return s}function e(q,p){m.startStyle(q);m.buildAlignment(p);m.buildBorder(p);m.buildFont(p);m.buildInterior(p);m.buildFormat(p);m.closeStyle();h+=m.toString()}function f(p){if(!p){return""}var q=k(p);if(typeof q==="undefined"){q=n();c[q]=p;e(q,p)}return q}};a.prototype=new b.jqx.dataAdapter.DataExportModuleBase();b.jqx.dataAdapter.ArrayExporter.extend("xls",new a())})(jQuery);(function(b){var a=function(){var e,c,d;this.beginFile=function(){e='<?xml version="1.0" encoding="UTF-8" ?>';e+="\n<table>"};this.beginHeader=function(){c=[]};this.appendHeaderCell=function(f,g){c.push(g)};this.endHeader=function(){};this.beginBody=function(g,f){};this.beginRow=function(){e+="\n\t<row>";d=0};this.appendBodyCell=function(f,h){var g=this.getFormat(h);f=this.formatData(f,g.type,g.formatString);e+="\n\t\t<"+c[d]+">"+f+"</"+c[d]+">";d++};this.endRow=function(){e+="\n\t</row>";d=0};this.endBody=function(){};this.endFile=function(){e+="\n</table>"};this.getFile=function(){return e}};a.prototype=new b.jqx.dataAdapter.DataExportModuleBase();b.jqx.dataAdapter.ArrayExporter.extend("xml",new a())})(jQuery);(function(d){var j=/[\\\"\x00-\x1f\x7f-\x9f\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g,l={"\b":"\\b","\t":"\\t","\n":"\\n","\f":"\\f","\r":"\\r",'"':'\\"',"\\":"\\\\"};function a(n){return'"'+n.replace(j,function(o){var p=l[o];return typeof p==="string"?p:"\\u"+("0000"+o.charCodeAt(0).toString(16)).slice(-4)})+'"'}function b(o){return o<10?"0"+o:o}function e(o){var n;if(isFinite(o.valueOf())){n=o.getUTCFullYear()+"-"+b(o.getUTCMonth()+1)+"-"+b(o.getUTCDate())+"T"+b(o.getUTCHours())+":"+b(o.getUTCMinutes())+":"+b(o.getUTCSeconds())+'Z"'}else{n="null"}return n}function g(q){var n=q.length,o=[],p;for(p=0;p<n;p++){o.push(h(p,q)||"null")}return"["+o.join(",")+"]"}function m(q){var o=[],p,n;for(p in q){if(Object.prototype.hasOwnProperty.call(q,p)){n=h(p,q);if(n){o.push(a(p)+":"+n)}}}return"{"+o.join(",")+"}"}function i(n){switch(Object.prototype.toString.call(n)){case"[object Date]":return e(n);case"[object Array]":return g(n)}return m(n)}function k(o,n){switch(n){case"string":return a(o);case"number":return isFinite(o)?o:"null";case"boolean":return o}return"null"}function h(o,n){var q=n[o],p=typeof q;if(q&&typeof q==="object"&&typeof q.toJSON==="function"){q=q.toJSON(o);p=typeof q}if(/(number|string|boolean)/.test(p)||(!q&&p==="object")){return k(q,p)}else{return i(q)}}function f(n){if(window.JSON&&typeof window.JSON.stringify==="function"){return window.JSON.stringify(n)}return h("",{"":n})}var c=function(){var n,o,p;this.beginFile=function(){o=[]};this.beginHeader=function(){};this.appendHeaderCell=function(q){};this.endHeader=function(){};this.beginBody=function(r,q){};this.beginRow=function(){p={}};this.appendBodyCell=function(r,q){p[q.text]=r};this.endRow=function(){o.push(p)};this.endBody=function(){};this.endFile=function(){n=f(o)};this.getFile=function(){return n}};c.prototype=new d.jqx.dataAdapter.DataExportModuleBase();d.jqx.dataAdapter.ArrayExporter.extend("json",new c())})(jQuery);