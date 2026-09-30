-- Recalculate and render a disposable copy; never save over the delivery workbook.
-- Usage: osascript numbers_qa.applescript INPUT.xlsx RECALCULATED.xlsx RENDERED.pdf
on run argv
    if (count of argv) is not 3 then error "Expected input, Excel export and PDF export paths"
    set inputFile to POSIX file (item 1 of argv)
    set excelFile to POSIX file (item 2 of argv)
    set pdfFile to POSIX file (item 3 of argv)
    tell application "Numbers Creator Studio"
        with timeout of 60 seconds
            set researchDocument to open inputFile
        end timeout
        try
            with timeout of 60 seconds
                export researchDocument to excelFile as Microsoft Excel with properties {exclude summary worksheet:true}
            end timeout
            with timeout of 60 seconds
                export researchDocument to pdfFile as PDF
            end timeout
        on error errorMessage number errorNumber
            close researchDocument saving no
            error errorMessage number errorNumber
        end try
        close researchDocument saving no
    end tell
end run
