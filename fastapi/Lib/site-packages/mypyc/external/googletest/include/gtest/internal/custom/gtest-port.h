// Copyright 2015, Google Inc.
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are
// met:
//
//     * Redistributions of source code must retain the above copyright
// notice, this list of conditions and the following disclaimer.
//     * Redistributions in binary form must reproduce the above
// copyright notice, this list of conditions and the following disclaimer
// in the documentation and/or other materials provided with the
// distribution.
//     * Neither the name of Google Inc. nor the names of its
// contributors may be used to endorse or promote products derived from
// this software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
// "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
// LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
// A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
// OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
// SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
// LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
// DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
// THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
// OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//
// Injection point for custom user configurations.
// The following macros can be defined:
//
//   Flag related macros:
//     GTEST_FLAG(flag_name)
//     GTEST_USE_OWN_FLAGFILE_FLAG_  - Define to 0 when the system provides its
//                                     own flagfile flag parsing.
//     GTEST_DECLARE_bool_(name)
//     GTEST_DECLARE_int32_(name)
//     GTEST_DECLARE_string_(name)
//     GTEST_DEFINE_bool_(name, default_val, doc)
//     GTEST_DEFINE_int32_(name, default_val, doc)
//     GTEST_DEFINE_string_(name, default_val, doc)
//
//   Test filtering:
//     GTEST_TEST_FILTER_ENV_VAR_ - The name of an environment variable that
//                                  will be used if --GTEST_FLAG(test_filter)
//                                  is not provided.
//
//   Logging:
//     GTEST_LOG_(severity)
//     GTEST_CHECK_(condition)
//     Functions LogToStderr() and FlushInfoLog() have to be provided too.
//
//   Threading:
//     GTEST_HAS_NOTIFICATION_ - Enabled if Notification is already provided.
//     GTEST_HAS_MUTEX_AND_THREAD_LOCAL_ - Enabled if Mutex and ThreadLocal are
//                                         already provided.
//     Must also provide GTEST_DECLARE_STATIC_MUTEX_(mutex) and
//     GTEST_DEFINE_STATIC_MUTEX_(mutex)
//
//     GTEST_EXCLUSIVE_LOCK_REQUIRED_(locks)
//     GTEST_LOCK_EXCLUDED_(locks)
//
// ** Custom implementation starts here **

#ifndef GTEST_INCLUDE_GTEST_INTERNAL_CUSTOM_GTEST_PORT_H_
#define GTEST_INCLUDE_GTEST_INTERNAL_CUSTOM_GTEST_PORT_H_

#endif  // GTEST_INCLUDE_GTEST_INTERNAL_CUSTOM_GTEST_PORT_H_
