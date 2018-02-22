Dim oXMLHTTP
Dim oStream

Set oXMLHTTP = CreateObject("MSXML2.XMLHTTP.3.0")

oXMLHTTP.Open "GET", "http://someserver/folder/file.pdf", False
oXMLHTTP.Send

If oXMLHTTP.Status = 200 Then
    Set oStream = CreateObject("ADODB.Stream")
    oStream.Open
    oStream.Type = 1
    oStream.Write oXMLHTTP.responseBody
    oStream.SaveToFile "c:\somefolder\file.pdf"
    oStream.Close
End If