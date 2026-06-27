@echo off
setlocal
chcp 65001
start "" /min powershell -ExecutionPolicy Bypass -Command "[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms') | Out-Null; [System.Windows.Forms.MessageBox]::Show('Messaggio di errore: Questo è un errore critico!', 'Errore', [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Error)"
endlocal
exit