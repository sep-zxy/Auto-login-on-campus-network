#Requires AutoHotkey v2.0
#SingleInstance Force

; ======================================================================================================================
;   GUI 布局定义
; ======================================================================================================================
MyGui := Gui("+AlwaysOnTop", "登录信息配置")
MyGui.SetFont("s10", "Microsoft YaHei UI")

MyGui.Add("Text", "w80", "账号:")
txtUsername := MyGui.Add("Edit", "w200")

MyGui.Add("Text", "w80", "密码:")
txtPassword := MyGui.Add("Edit", "w200 Password")

MyGui.Add("Text", "w80", "运营商:")
txtOperator := MyGui.Add("Edit", "w200")

btnSave := MyGui.Add("Button", "w100 h28 Default", "保存配置")

; --- 事件绑定 ---
btnSave.OnEvent("Click", SaveConfig)
MyGui.OnEvent("Close", (*) => ExitApp())

LoadConfig()
MyGui.Show("w320")
return


; ======================================================================================================================
;   函数定义
; ======================================================================================================================

SaveConfig(*)
{
    global txtUsername, txtPassword, txtOperator

    if (txtUsername.Value = "" or txtPassword.Value = "")
    {
        MsgBox("账号和密码不能为空！", "错误", 48)
        return
    }

    configMap := Map(
        "username", txtUsername.Value,
        "password", txtPassword.Value,
        "operator_label", txtOperator.Value
    )
    jsonString := MapToJSON(configMap)

    try
    {
        File := FileOpen("config.json", "w", "UTF-8")
        File.Write(jsonString)
        File.Close()
        MsgBox("配置已成功保存到 config.json！", "成功", 64)
        ExitApp
    }
    catch
    {
        MsgBox("无法写入 config.json 文件，请检查权限！", "保存失败", 16)
    }
}

LoadConfig()
{
    global txtUsername, txtPassword, txtOperator
    configFile := "config.json"
    if !FileExist(configFile)
    {
        txtOperator.Value := "巢湖学院"
        return
    }

    try
    {
        jsonString := FileRead(configFile, "UTF-8")
        username := RegExMatch(jsonString, '"username":\s*"([^"]*)"', &match) ? match[1] : ""
        password := RegExMatch(jsonString, '"password":\s*"([^"]*)"', &match) ? match[1] : ""
        operator := RegExMatch(jsonString, '"operator_label":\s*"([^"]*)"', &match) ? match[1] : "巢湖学院"

        txtUsername.Value := username
        txtPassword.Value := password
        txtOperator.Value := operator
    }
    catch
    {
        txtOperator.Value := "巢湖学院"
    }
}

; *** 核心修正：为解决罕见的 .Join() 方法错误，我们改用手动循环来拼接字符串 ***
MapToJSON(mapObj)
{
    jsonBody := ""
    isFirst := true
    for key, value in mapObj
    {
        if !isFirst
        {
            jsonBody .= ","
        }
        
        escapedValue := StrReplace(value, "\", "\\")
        escapedValue := StrReplace(escapedValue, '"', '\"')
        
        jsonBody .= '"' . key . '": "' . escapedValue . '"'
        isFirst := false
    }
    return "{" . jsonBody . "}"
}