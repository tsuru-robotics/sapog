/*
    ChibiOS - Copyright (C) 2006..2015 Giovanni Di Sirio.

    This file is part of ChibiOS.

    ChibiOS is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License, or
    (at your option) any later version.

    ChibiOS is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

/**
 * @file    chstreams.h
 * @brief   Data streams.
 * @details This header defines abstract interfaces useful to access generic
 *          data streams in a standardized way.
 *
 * @addtogroup data_streams
 * @details This module define an abstract interface for generic data streams.
 *          Note that no code is present, just abstract interfaces-like
 *          structures, you should look at the system as to a set of
 *          abstract C++ classes (even if written in C). This system
 *          has then advantage to make the access to data streams
 *          independent from the implementation logic.<br>
 *          The stream interface can be used as base class for high level
 *          object types such as files, sockets, serial ports, pipes etc.
 * @{
 */

#ifndef _CHSTREAMS_H_
#define _CHSTREAMS_H_


/**
 * @name    Macro Functions (BaseSequentialStream)
 * @{
 */
/**
 * @brief   Sequential Stream write.
 * @details The function writes data from a buffer to a stream.
 *
 * @param[in] ip        pointer to a @p BaseSequentialStream or derived class
 * @param[in] bp        pointer to the data buffer
 * @param[in] n         the maximum amount of data to be transferred
 * @return              The number of bytes transferred. The return value can
 *                      be less than the specified number of bytes if an
 *                      end-of-file condition has been met.
 *
 * @api
 */
#define chSequentialStreamWrite(ip, bp, n) ((ip)->vmt->write(ip, bp, n))

/**
 * @brief   Sequential Stream read.
 * @details The function reads data from a stream into a buffer.
 *
 * @param[in] ip        pointer to a @p BaseSequentialStream or derived class
 * @param[out] bp       pointer to the data buffer
 * @param[in] n         the maximum amount of data to be transferred
 * @return              The number of bytes transferred. The return value can
 *                      be less than the specified number of bytes if an
 *                      end-of-file condition has been met.
 *
 * @api
 */
#define chSequentialStreamRead(ip, bp, n) ((ip)->vmt->read(ip, bp, n))

/**
 * @brief   Sequential Stream blocking byte write.
 * @details This function writes a byte value to a channel. If the channel
 *          is not ready to accept data then the calling thread is suspended.
 *
 * @param[in] ip        pointer to a @p BaseSequentialStream or derived class
 * @param[in] b         the byte value to be written to the channel
 *
 * @return              The operation status.
 * @retval Q_OK         if the operation succeeded.
 * @retval Q_RESET      if an end-of-file condition has been met.
 *
 * @api
 */
#define chSequentialStreamPut(ip, b) ((ip)->vmt->put(ip, b))

/**
 * @brief   Sequential Stream blocking byte read.
 * @details This function reads a byte value from a channel. If the data
 *          is not available then the calling thread is suspended.
 *
 * @param[in] ip        pointer to a @p BaseSequentialStream or derived class
 *
 * @return              A byte value from the queue.
 * @retval Q_RESET      if an end-of-file condition has been met.
 *
 * @api
 */
#define chSequentialStreamGet(ip) ((ip)->vmt->get(ip))
/** @} */

#endif /* _CHSTREAMS_H_ */

/** @} */
