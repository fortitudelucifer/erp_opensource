; core_erp.iss - CORE ERP Inno Setup 安装脚本 v2.0.0
; 使用方法: 用 Inno Setup Compiler 打开此文件并编译
;
; 前提: 先运行 python installer/build.py 生成 build/ 目录
; v2.0: 集成 NSSM，以 Windows 服务形式后台运行

[Setup]
AppName=CORE ERP
AppVersion=3.0.0
AppPublisher=CORE ERP Team
AppPublisherURL=https://github.com/fortitudelucifer/erp_opensource
DefaultDirName=C:\CoreERP
DefaultGroupName=CORE ERP
OutputDir=output
OutputBaseFilename=CoreERP-Setup-v3.0.0
Compression=lzma2
SolidCompression=yes
SetupIconFile=
; 需要管理员权限（安装服务、防火墙规则）
PrivilegesRequired=admin
AllowNoIcons=yes

[Languages]
Name: "chinesesimplified"; MessagesFile: "compiler:Languages\ChineseSimplified.isl"

[Files]
; 复制 build/ 目录下的所有文件（含 nssm.exe）
Source: "build\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; \
    Excludes: "data\erp.db,data\config.json"
; data 目录单独处理：仅在不存在时创建
Source: "build\data\*"; DestDir: "{app}\data"; Flags: onlyifdoesntexist recursesubdirs createallsubdirs

[Dirs]
; 确保 data 目录存在且在卸载时不删除（保留用户数据）
Name: "{app}\data"; Flags: uninsneveruninstall
Name: "{app}\data\uploads"; Flags: uninsneveruninstall

[Icons]
; 桌面快捷方式 — 仅打开浏览器（服务在后台运行）
Name: "{userdesktop}\CORE ERP"; Filename: "{app}\open.bat"; WorkingDir: "{app}"; \
    Comment: "打开 CORE ERP 企业管理系统"
; 开始菜单
Name: "{group}\CORE ERP"; Filename: "{app}\open.bat"; WorkingDir: "{app}"
Name: "{group}\CORE ERP (手动模式)"; Filename: "{app}\start.bat"; WorkingDir: "{app}"
Name: "{group}\卸载 CORE ERP"; Filename: "{uninstallexe}"

[Run]
; === 安装完成后：注册并启动 Windows 服务 ===

; 先清理可能存在的旧服务（覆盖安装场景）
Filename: "{app}\nssm.exe"; Parameters: "stop CoreERP"; \
    Flags: runhidden; StatusMsg: "停止旧服务..."; Check: ServiceExists
Filename: "{app}\nssm.exe"; Parameters: "remove CoreERP confirm"; \
    Flags: runhidden; StatusMsg: "移除旧服务..."; Check: ServiceExists

; 注册新服务
Filename: "{app}\nssm.exe"; Parameters: "install CoreERP ""{app}\python\python.exe"" ""{app}\launcher.py"" --no-browser --port 8000"; \
    Flags: runhidden; StatusMsg: "注册 CORE ERP 服务..."
; 设置工作目录
Filename: "{app}\nssm.exe"; Parameters: "set CoreERP AppDirectory ""{app}"""; \
    Flags: runhidden
; 设置显示名称
Filename: "{app}\nssm.exe"; Parameters: "set CoreERP DisplayName ""CORE ERP Server"""; \
    Flags: runhidden
; 设置描述
Filename: "{app}\nssm.exe"; Parameters: "set CoreERP Description ""CORE ERP 企业资源管理系统 - 后台服务"""; \
    Flags: runhidden
; 设置开机自启
Filename: "{app}\nssm.exe"; Parameters: "set CoreERP Start SERVICE_AUTO_START"; \
    Flags: runhidden
; 设置日志输出
Filename: "{app}\nssm.exe"; Parameters: "set CoreERP AppStdout ""{app}\data\service.log"""; \
    Flags: runhidden
Filename: "{app}\nssm.exe"; Parameters: "set CoreERP AppStderr ""{app}\data\service.log"""; \
    Flags: runhidden
; 日志文件追加模式
Filename: "{app}\nssm.exe"; Parameters: "set CoreERP AppStdoutCreationDisposition 4"; \
    Flags: runhidden
Filename: "{app}\nssm.exe"; Parameters: "set CoreERP AppStderrCreationDisposition 4"; \
    Flags: runhidden

; 启动服务
Filename: "{app}\nssm.exe"; Parameters: "start CoreERP"; \
    Flags: runhidden; StatusMsg: "启动 CORE ERP 服务..."

; 添加 Windows 防火墙规则
Filename: "netsh"; Parameters: "advfirewall firewall add rule name=""CORE ERP Server"" dir=in action=allow protocol=TCP localport=8000"; \
    Flags: runhidden; StatusMsg: "配置防火墙规则..."

; 安装完成后打开浏览器
Filename: "{app}\open.bat"; Description: "打开 CORE ERP"; \
    WorkingDir: "{app}"; Flags: nowait postinstall skipifsilent shellexec

[UninstallRun]
; 卸载时停止并移除服务
Filename: "{app}\nssm.exe"; Parameters: "stop CoreERP"; \
    Flags: runhidden; RunOnceId: "StopService"
Filename: "{app}\nssm.exe"; Parameters: "remove CoreERP confirm"; \
    Flags: runhidden; RunOnceId: "RemoveService"
; 删除防火墙规则
Filename: "netsh"; Parameters: "advfirewall firewall delete rule name=""CORE ERP Server"""; \
    Flags: runhidden; RunOnceId: "RemoveFirewall"

[UninstallDelete]
; 卸载时清理缓存，但保留 data/
Type: filesandordirs; Name: "{app}\core\__pycache__"
Type: filesandordirs; Name: "{app}\python\Lib\__pycache__"
Type: files; Name: "{app}\data\service.log"

[Code]
function ServiceExists(): Boolean;
var
  ResultCode: Integer;
begin
  Exec('sc.exe', 'query CoreERP', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
  Result := (ResultCode = 0);
end;
