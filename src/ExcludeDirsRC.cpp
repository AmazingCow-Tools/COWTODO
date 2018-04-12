// Header
#include "ExcludeDirsRC.h"
// std
#include <iterator> // std::back_inserter
// AmazingCow Libs
#include "acow/algo.h"
#include "acow/cpp_goodies.h"
#include "CoreDir/CoreDir.h"
#include "CoreFile/CoreFile.h"
#include "CoreFS/CoreFS.h"
// COWTODO
#include "Logger.h"

//----------------------------------------------------------------------------//
// Constants                                                                  //
//----------------------------------------------------------------------------//
constexpr auto kPathDir  = "~/.cowtodorc";
constexpr auto kPathFile = "cowtodorc.txt";


//----------------------------------------------------------------------------//
// Internal Vars                                                              //
//----------------------------------------------------------------------------//
acow_global_variable std::vector<std::string> gPaths;
acow_global_variable bool                     gInitialized = false;


//----------------------------------------------------------------------------//
// Helper Functions                                                           //
//----------------------------------------------------------------------------//
acow_internal_function std::string 
GetFolderFullpath() noexcept 
{
    auto folder_fullpath = CoreFS::ExpandUserAndMakeAbs(kPathDir);
    return folder_fullpath;
}

acow_internal_function std::string 
GetFileFullpath() noexcept 
{    
    auto file_fullpath = CoreFS::Join(GetFolderFullpath(), {kPathFile});
    return file_fullpath;
}

acow_internal_function void 
EnsureRCFile() noexcept
{
    auto folder_fullpath = GetFolderFullpath();
    auto file_fullpath   = GetFileFullpath  ();

    //--------------------------------------------------------------------------
    // Check if we have the RC file and dir. 
    //   If not create one.
    if(!CoreFS::IsDir(folder_fullpath)) {
        GetLogger()->Info(
            "Missing folder at: (%s)\n  Creating one now.",
            folder_fullpath
        );
        
        CoreDir ::CreateDirectory(folder_fullpath);
        CoreFile::CreateText     (file_fullpath);
    }
}


//----------------------------------------------------------------------------//
// Implementation                                                             //
//----------------------------------------------------------------------------//
void 
ExcludeDirsRC::Initialize() noexcept
{    
    if(gInitialized) { return; }
    gInitialized = true;

    EnsureRCFile();
    
    // Read the paths.
    gPaths = CoreFile::ReadAllLines(GetFileFullpath());

    // Clean them up.
    acow::algo::for_each(
        gPaths, 
        [](std::string &path){ CoreString::Trim(path); 
    });

    acow::algo::sort_and_unique(gPaths);
    acow::algo::remove_if(
        gPaths, 
        [](const std::string line){ 
            return line.empty();
        }, true
    );
}

void 
ExcludeDirsRC::Save() noexcept
{
    EnsureRCFile();
    CoreFile::WriteAllLines(GetFileFullpath(), gPaths);
}

void 
ExcludeDirsRC::AddPaths(const std::vector<std::string> &paths) noexcept
{
    acow::algo::copy_insert(paths, gPaths);
    acow::algo::sort_and_unique(gPaths);
}

void 
ExcludeDirsRC::RemovePaths(const std::vector<std::string> &paths) noexcept
{
    auto new_paths = std::vector<std::string>();
    new_paths.reserve(gPaths.size());
    
    std::set_difference(
        std::begin(gPaths), 
        std::end  (gPaths), 
        std::begin(paths ),
        std::end  (paths ), 
        std::back_inserter(new_paths)
    );

    gPaths.swap(new_paths);
}

const std::vector<std::string>&
ExcludeDirsRC::GetExcludedPaths() noexcept
{
    return gPaths;
}

