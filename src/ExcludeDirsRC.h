#pragma once

// std
#include <string>
#include <vector>


namespace ExcludeDirsRC 
{
    void Initialize() noexcept;
    void Save() noexcept;

    void AddPaths   (const std::vector<std::string> &paths) noexcept;   
    void RemovePaths(const std::vector<std::string> &paths) noexcept;

    const std::vector<std::string>& GetExcludedPaths() noexcept;

} // namespace ExcludeDirsRC