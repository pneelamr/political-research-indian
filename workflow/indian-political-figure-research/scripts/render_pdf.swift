// Render pages from a real application's PDF export, without reflowing cells.
// swift render_pdf.swift input.pdf output-directory [page-number ...]
import Foundation
import PDFKit
import AppKit

let args = CommandLine.arguments
guard args.count >= 3, let document = PDFDocument(url: URL(fileURLWithPath: args[1])) else {
    fatalError("Expected readable PDF and output directory")
}
let directory = URL(fileURLWithPath: args[2])
try FileManager.default.createDirectory(at: directory, withIntermediateDirectories: true)
var pages: [[String: Any]] = []
for index in 0..<document.pageCount {
    let page = document.page(at: index)!
    let bounds = page.bounds(for: .mediaBox)
    pages.append(["page": index+1, "width": bounds.width, "height": bounds.height, "text": page.string ?? ""])
}
try JSONSerialization.data(withJSONObject: pages, options: [.prettyPrinted, .sortedKeys]).write(to: directory.appendingPathComponent("pages.json"))
for number in args.dropFirst(3).compactMap({Int($0)}) {
    guard number > 0 && number <= document.pageCount else { fatalError("Invalid page") }
    let page = document.page(at: number-1)!
    let bounds = page.bounds(for: .mediaBox)
    let height = min(bounds.height, 800)
    for (region, y) in [("top", bounds.maxY-height), ("middle", bounds.midY-height/2), ("bottom", bounds.minY)] {
        page.setBounds(NSRect(x: bounds.minX, y: y, width: bounds.width, height: height), for: .cropBox)
        let image = page.thumbnail(of: NSSize(width: 2000, height: 2000*height/bounds.width), for: .cropBox)
        let bitmap = NSBitmapImageRep(data: image.tiffRepresentation!)!
        try bitmap.representation(using: .png, properties: [:])!.write(to: directory.appendingPathComponent("page-\(number)-\(region).png"))
    }
}
print("PDF pages: \(document.pageCount); rendered: \(max(0,args.count-3))")
