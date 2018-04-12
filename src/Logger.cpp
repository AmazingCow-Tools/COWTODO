// Header
#include "Logger.h"

CoreLog::Logger* 
GetLogger() noexcept
{
    acow_local_persist CoreLog::Logger s_logger;
    return &s_logger;
}