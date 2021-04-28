#include <QApplication>
#include <QFileDialog>
#include <QFileSystemWatcher>
#include <QTextStream>
#include <QRegularExpression>
#include <QMessageBox>

//Script that is inserted into HTML file selected by user.
QString javascript = "\r\n\r\n<!--DO NOT MODIFY THIS SCRIPT OR RELOAD WON'T WORK!! YOU CAN SAFELY DELETE IT WHEN YOUR SITE IS FINISHED!-->\r\n"
            "<script>\r\n" 
            "\tif (\"WebSocket\" in window) {\r\n"
	        "\t\tvar ws = new WebSocket(\"ws://localhost:5000/%1\");\r\n\r\n"
            "\t\tws.onmessage = function(evt) {\r\n"
		    "\t\t\tvar msg = evt.data;\r\n"
		    "\t\t\tif (msg == \"Reload\") {\r\n"
			"\t\t\t\tws.close();\r\n"
			"\t\t\t\tlocation.reload();\r\n"
			"\t\t\t\treturn;\r\n"
		    "\t\t\t}\r\n"
	        "\t\t}\r\n"
            "\t}\r\n"
            "</script>\r\n";

//Slot that handles QFileSystemWatcher::fileChanged signal
void fileChanged(const QString&) {
    QTextStream str(stdout);
    str << "Reload site\n";
}

//Function that checks if command line arguments contains arg string.
bool argExists(char* argv[], int argc, char* arg) {
    for (int i = 0; i < argc; i++)
        if (QString(argv[i]) == arg)
            return true;

    return false;
}

//Function that returns the HTML file that user previously selected, from command line arguments.
QString extractPathFromArgs(char* argv[], int argc) {
    for (int i = 1; i < argc; i++)
        if (QFileInfo(argv[i]).exists() && (QString(argv[i]).endsWith(".html") || QString(argv[i]).endsWith(".htm")))
            return argv[i];

    return QString();
}

//Main function.
int main(int argc, char *argv[]){
    QApplication a(argc, argv);

    if (argExists(argv, argc, "--authorized: sadn29ue299sa[0as9yy19qldSDNX[OOJASPE29QE39G33QGLJLASBPA229")) {
        QString file = extractPathFromArgs(argv, argc);
            
        if(file.isNull())
            file = QFileDialog::getOpenFileName(nullptr, "Choose your site", "", "HTML (*.html *.htm)");

        if (file != "") {
            QFile fileObject(file);
            QStringList extFiles;

            QStringList list;
            list << file;

            QString path = file.remove("/" + file.split("/").last());

            if (fileObject.open(QFile::ReadWrite)) {
                QString content = QString::fromLatin1(fileObject.readAll());

                javascript = javascript.arg(list[0].split("/").last());
                if (!content.contains(javascript)) {
                    int bodyIndex = content.indexOf("</body>");
                    fileObject.seek(bodyIndex);
                    fileObject.write("\n" + javascript.toUtf8());
                    fileObject.write("\t</body>\r\n</html>");
                }
                fileObject.close();

                QRegularExpression exp("href[ \t]{0,}=[ \t]{0,}\"(.{1,}\\.css)\"|src[ \t]{0,}=[ \t]{0,}\"(.{1,}\\.js)\"");
                QRegularExpressionMatchIterator i = exp.globalMatch(content);
                int groupIndex;

                while (i.hasNext()) {
                    QRegularExpressionMatch match = i.next();
                    if (match.hasMatch()) {
                        if (match.captured(0).startsWith("src"))
                            groupIndex = 2;
                        else
                            groupIndex = 1;
                        extFiles << path + "/" + match.captured(groupIndex);
                    }
                }
            }

            list << extFiles;

            QFileSystemWatcher* watcher = new QFileSystemWatcher;
            watcher->addPaths(list);
            QObject::connect(watcher, &QFileSystemWatcher::fileChanged, fileChanged);

            QTextStream out(stdout);
            out << list[0] + "\n";
            out.flush();

            return a.exec();
        }
        else {
            QTextStream out(stdout);
            out << "\n";

            return 0;
        }
    }
    else {
        QMessageBox::critical(nullptr, "Error", "App was not authorized to run!");
        return 0;
    }
}
