import platform

def get_normalized_platform() -> str:
    normalized_system = platform.system().lower()
    if normalized_system == 'darwin':    
        return 'mac os'
    return normalized_system
            
def is_platform_supported() -> bool:
    supported_platforms = {
        'linux',
        'windows',
        'mac os'
    }
    system = get_normalized_platform()
    if system not in supported_platforms:
        return False
    return True

def get_platform() -> str:
    return platform.system()
    
#TODO: add a way to collect platform specific code for makefile

    
    