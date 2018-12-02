Sub totalStock()
Dim i As Long
Dim ticker As String
Dim stock_total As Variant
Dim Summary_Table_Row As Integer
Dim summary_max_table_row As Integer
Dim LastRow As Long
Dim row_head1 As String
Dim ws As Worksheet
Dim stock_open_value As Double
Dim stock_close_value As Double
Dim stock_change As Double
Dim stock_percent_change As Double
Dim max_percent_increase As Double
Dim max_percent_decrease As Double
Dim max_stock_total As Variant
Dim last_row As Long

Dim row_head2 As String
        
For Each ws In Worksheets
    stock_total = 0
    row_head1 = "Ticker"
    row_head2 = "Total Stock Volume"
    ws.Range("I1").Value = row_head1
    ws.Range("J1").Value = "Yearly Change"
    ws.Range("K1").Value = "Percentage Change"
    ws.Range("L1").Value = row_head2
    ws.Range("O2").Value = "Greatest % Increase"
    ws.Range("O3").Value = "Greatest % Decrease"
    ws.Range("O4").Value = "Greatest Total Volume"
    ws.Range("P1").Value = "Ticker"
    ws.Range("Q1").Value = "Value"
    LastRow = Cells(Rows.Count, 1).End(xlUp).Row
    stock_open_value = ws.Cells(2, 3).Value
    
    Summary_Table_Row = 2
    summary_max_table_row = 2
    
    For i = 2 To LastRow
        If ws.Cells(i + 1, 1).Value <> ws.Cells(i, 1).Value Then
            ticker = ws.Cells(i, 1).Value
            stock_total = stock_total + ws.Cells(i, 7).Value
            ws.Range("I" & Summary_Table_Row).Value = ticker
            ws.Range("L" & Summary_Table_Row).Value = stock_total
            stock_change = stock_close_value - stock_open_value
            ws.Range("J" & Summary_Table_Row).Value = stock_change
            If stock_change >= 0 Then
                ws.Range("J" & Summary_Table_Row).Interior.ColorIndex = 4
            Else
                ws.Range("J" & Summary_Table_Row).Interior.ColorIndex = 3
            End If
            
            If stock_open_value <> 0 Then
                stock_percent_change = stock_change / stock_open_value
                ws.Range("K" & Summary_Table_Row).Value = Format(CStr(stock_percent_change), "percent")
            Else
                ws.Range("K" & Summary_Table_Row).Value = Format(CStr(0), "percent")
            End If
            
            stock_total = 0
            Summary_Table_Row = Summary_Table_Row + 1
            stock_open_value = ws.Cells(i + 1, 3).Value
        Else
            stock_total = stock_total + ws.Cells(i, 7).Value
            stock_close_value = ws.Cells(i + 1, 6).Value
        End If

    Next i
    
    last_row_percent = ws.Cells(Rows.Count, 11).End(xlUp).Row
    last_row_stock = ws.Cells(Rows.Count, 12).End(xlUp).Row
    
    '"%" & worksheetFunction.Max(ws.range("K2:K" & last_row)) * 100
    max_percent_change = WorksheetFunction.Max(ws.Range("K2:K" & last_row_percent))
    max_percent_change = Format(max_percent_change, "Percent")
    max_percent_ticker_index = WorksheetFunction.Match(WorksheetFunction.Max(ws.Range("K2:K" & last_row_percent)), ws.Range("K2:K" & last_row_percent), 0)
    max_percent_ticker = ws.Range("I" & max_percent_ticker_index + 1).Value
    
    min_percent_change = WorksheetFunction.Min(ws.Range("K2:K" & last_row_percent))
    min_percent_change = Format(min_percent_change, "Percent")
    min_percent_ticker_index = WorksheetFunction.Match(WorksheetFunction.Min(ws.Range("K2:K" & last_row_percent)), ws.Range("K2:K" & last_row_percent), 0)
    min_percent_ticker = ws.Range("I" & min_percent_ticker_index + 1).Value
    
    max_stock_total = WorksheetFunction.Max(ws.Range("L2:L" & last_row_stock))
    max_stock_ticker_index = WorksheetFunction.Match(WorksheetFunction.Max(ws.Range("L2:L" & last_row_stock)), ws.Range("L2:L" & last_row_stock), 0)
    max_stock_ticker = ws.Range("I" & max_stock_ticker_index + 1).Value
    
    ws.Range("P2").Value = max_percent_ticker
    ws.Range("q2").Value = max_percent_change
    ws.Range("P3").Value = min_percent_ticker
    ws.Range("q3").Value = min_percent_change
    ws.Range("P4").Value = max_stock_ticker
    ws.Range("q4").Value = max_stock_total
    ws.Range("o1").Value = ""
    
    ws.Columns(9).AutoFit
    ws.Columns(10).AutoFit
    ws.Columns(11).AutoFit
    ws.Columns(12).AutoFit
    ws.Columns(15).AutoFit
    ws.Columns(16).AutoFit
    ws.Columns(17).AutoFit
Next ws
End Sub

