## git
- 本地分支改名
 	    
 	    git branch -m master  new_master
- 当前分支push到另一远程分支
 	    
 	    git push origin new_master
- git rebase流程
        
        1. git checkout master
        2. git pull
        3. git checkout my_branch
        4. git rebase master
        5. git status # 查看冲突文件
        6. 对冲突文件进行修改
        7. git add .     # 确认修改完成
        8. git rebase —continue
        9. 循环5.6.7 直至没有冲突
        10. git push -force   此命令万分小心，最好提前分出一个备用分支，防止push出错
- 显示所有远程分支
        
        git branch -r 
- 删除本地分支
 	    
 	    git branch -d my_branch
 	    git branch -D my_branch    
- 修改跟踪远程分支

        git branch my_branch --set-upstream-to origin/my_new_branch
-  拉取远端代码强行覆盖本地代码  一般用于rebase之后使用
 	    
 	    git fetch --all && git reset --hard origin/my_branch && git pull
- 本地分支test提交到远程仓库，并作为远程仓库A分支
        
        git push origin test:A
- 看提交记录
            
        git log 
        git log -2 看最近两条提交
        强制恢复和远程分支一致的位置
        git reset —hard origin/my_branch
        强制恢复到某一位置
        git reset —hard 261accd4a
- 查看远程分支
     
        git branch -ｒ
- 删除远程分支
        
        git branch -r -d origin/branch-name
        git push origin :branch-name
