REM 供本地在網頁使用工具類頁面，其他頁面直接點擊可用。本地服務器需要python支持

@echo off
REM 使用python啓動本地服務器
start python -m http.server 8262

REM 進入瀏覽器
start http://localhost:8262/