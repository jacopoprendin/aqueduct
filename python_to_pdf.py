import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtPrintSupport import  QPrinter
from PyQt5.QtWebKitWidgets import QWebView
 
app = QApplication(sys.argv)
html="""
<!DOCTYPE html>
<html>
<head>
<style>
p.error {
    color: red;
}
</style>
</head>
<body>

<p>This is a paragraph.</p>
<p>This is a paragraph.</p>
<p class="error">I am different.</p>
<p>This is a paragraph.</p>
<p class="error">I am different too.</p>

</body>
</html>

"""
web = QWebView()
web.setHtml(html)
 
printer = QPrinter()
printer.setPageSize(QPrinter.A4)
printer.setOutputFormat(QPrinter.PdfFormat)
printer.setOutputFileName("./provaacazzo.pdf")
web.print_(printer)
app.exit()
