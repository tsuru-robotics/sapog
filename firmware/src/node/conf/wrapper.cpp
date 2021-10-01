#include "wrapper.hpp"

converter_type find_converter(const char *name)
{
    for (auto &pair: converters)
    {
        const char *current_name = pair.first;
        if (strcmp(current_name, name) == 0)
        {
            converter_type *converter = &(pair.second);
            return *converter;
        }
    }
    // In case there isn't a matching converter, return one that returns an empty value.
    // the returned value is basically selected to be uavcan.primitive.Empty.1.0
    return [](float input) {
        (void) input;
        return value_type{};
    };
}
