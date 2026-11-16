// Crop an actual spreadsheet-application PDF without reflowing any cell.
// Usage: swift render_regions.swift input.pdf directory page:x:top:width:height ...
import Foundation
import AppKit
import PDFKit
let args=CommandLine.arguments
guard args.count >= 4, let doc=PDFDocument(url:URL(fileURLWithPath:args[1])) else { fatalError("Input PDF required") }
let directory=URL(fileURLWithPath:args[2])
try FileManager.default.createDirectory(at:directory,withIntermediateDirectories:true)
for (i,arg) in args.dropFirst(3).enumerated() {
    let v=arg.split(separator:":").compactMap { Double($0) }
    guard v.count==5,let page=doc.page(at:Int(v[0])-1) else {fatalError("Invalid region")}
    let bounds=page.bounds(for:.mediaBox)
    let crop=NSRect(x:v[1],y:bounds.height-v[2]-v[4],width:v[3],height:v[4])
    page.setBounds(crop,for:.cropBox)
    let img=page.thumbnail(of:NSSize(width:2000,height:2000*v[4]/v[3]),for:.cropBox)
    let bitmap=NSBitmapImageRep(data:img.tiffRepresentation!)!
    try bitmap.representation(using:.png,properties:[:])!.write(to:directory.appendingPathComponent("region-\(i+1)-page-\(Int(v[0])).png"))
}
print("Rendered \(args.count-3) unchanged PDF regions")
