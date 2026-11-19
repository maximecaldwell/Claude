// Dump a PDF's text layer, page by page, with a form feed between pages.
import Foundation
import PDFKit
let url = URL(fileURLWithPath: CommandLine.arguments[1])
guard let doc = PDFDocument(url: url) else { print("load failed"); exit(1) }
for i in 0..<doc.pageCount {
    print(doc.page(at: i)?.string ?? "")
    print("\u{0C}")
}
