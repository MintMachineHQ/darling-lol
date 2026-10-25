from pathlib import Path
import getpass,json,os,subprocess
ROOT=Path(__file__).resolve().parent.parent
LFS_POINTER=b'version https://git-lfs.github.com/spec/v1\n'

def lfs_pointer(path):
    """True when a worktree file still holds Git LFS pointer text, not its object."""
    try:
        with open(path,'rb') as handle:head=handle.read(200)
    except OSError:
        return False
    return head.startswith(LFS_POINTER) and b'\nsize ' in head

def lfs_pointers(repo):
    """LFS-tracked files still checked out as pointer text instead of their object.

    The marker from `git lfs ls-files` is not enough: it reports * (object present)
    when pointer text happens to be the same size as the object.
    """
    out=subprocess.run(['git','-C',str(repo),'lfs','ls-files','--name-only'],
                       text=True,capture_output=True).stdout
    return [name for name in out.splitlines() if lfs_pointer(Path(repo)/name)]

def configuration():
    file=ROOT/'build/config.json'
    if file.exists():return json.loads(file.read_text())
    username=getpass.getuser()
    return {'project_root':str(ROOT),'host_home':str(Path.home()),'prefix':str(Path.home()/'.darling'),'guest_user':username,'guest_home':'/Users/'+username,'sdk':'/usr/local/libexec/darling'}

def render(text,config=None):
    c=config or configuration()
    for token,key in [('PROJECT_ROOT','project_root'),('HOST_HOME','host_home'),('DPREFIX','prefix'),('GUEST_USER','guest_user'),('GUEST_HOME','guest_home'),('DARLING_SDK','sdk')]:
        text=text.replace('@'+token+'@',c[key])
    return text
