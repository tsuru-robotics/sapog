#ifndef FIRMWARE_ISTORAGEBACKEND_HPP
#define FIRMWARE_ISTORAGEBACKEND_HPP
/**
 * This interface abstracts the configuration storage.
 */
namespace os::config
{
class IStorageBackend
{
public:
    virtual ~IStorageBackend()
    {}

    virtual int read(std::size_t offset, void *data, std::size_t len) = 0;

    virtual int write(std::size_t offset, const void *data, std::size_t len) = 0;

    virtual int erase() = 0;
};
}

#endif //FIRMWARE_ISTORAGEBACKEND_HPP
