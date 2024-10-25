/* -*- Mode: C++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*- */
/* ***** BEGIN LICENSE BLOCK *****
 * Version: MPL 1.1/GPL 2.0/LGPL 2.1
 *
 * The contents of this file are subject to the Mozilla Public License Version
 * 1.1 (the "License"); you may not use this file except in compliance with
 * the License. You may obtain a copy of the License at
 * http://www.mozilla.org/MPL/
 *
 * Software distributed under the License is distributed on an "AS IS" basis,
 * WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
 * for the specific language governing rights and limitations under the
 * License.
 *
 * The Original Code is the Netscape Portable Runtime (NSPR).
 *
 * The Initial Developer of the Original Code is
 * Netscape Communications Corporation.
 * Portions created by the Initial Developer are Copyright (C) 1998-2000
 * the Initial Developer. All Rights Reserved.
 *
 * Contributor(s):
 *  innotek
 *
 * Alternatively, the contents of this file may be used under the terms of
 * either the GNU General Public License Version 2 or later (the "GPL"), or
 * the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
 * in which case the provisions of the GPL or the LGPL are applicable instead
 * of those above. If you wish to allow use of your version of this file only
 * under the terms of either the GPL or the LGPL, and not to allow others to
 * use your version of this file under the terms of the MPL, indicate your
 * decision by deleting the provisions above and replace them with the notice
 * and other provisions required by the GPL or the LGPL. If you do not delete
 * the provisions above, a recipient may use your version of this file under
 * the terms of any one of the MPL, the GPL or the LGPL.
 *
 * ***** END LICENSE BLOCK ***** */

#ifndef nspr_vboxcfg___
#define nspr_vboxcfg___

#ifdef VBOX
# include <iprt/cdefs.h>

#ifdef RT_LITTLE_ENDIAN
#undef IS_BIG_ENDIAN
# define  IS_LITTLE_ENDIAN 1
#elif defined(RT_BIG_ENDIAN)
# undef IS_LITTLE_ENDIAN
# define  IS_BIG_ENDIAN 1
#else
# error "Unknown endianess"
#endif
#else
/* Assume little endian hosts as VBox doesn't run on anything else right now. */
# undef IS_BIG_ENDIAN
# define IS_LITTLE_ENDIAN
#endif

#define HAVE_LONG_LONG

#define PR_BYTES_PER_BYTE   1
#define PR_BYTES_PER_SHORT  2
#define PR_BYTES_PER_INT    4
#define PR_BYTES_PER_INT64  8
#if defined(RT_ARCH_AMD64) || defined(RT_ARCH_ARM64)
# define PR_BYTES_PER_LONG   8
#else
# define PR_BYTES_PER_LONG   4
#endif
#define PR_BYTES_PER_FLOAT  4
#define PR_BYTES_PER_DOUBLE 8

#define PR_BITS_PER_BYTE    8
#define PR_BITS_PER_SHORT   16
#define PR_BITS_PER_INT     32
#define PR_BITS_PER_INT64   64
#if defined(RT_ARCH_AMD64) || defined(RT_ARCH_ARM64)
# define PR_BITS_PER_LONG    64
#else
# define PR_BITS_PER_LONG    32
#endif
#define PR_BITS_PER_FLOAT   32
#define PR_BITS_PER_DOUBLE  64

#define PR_BITS_PER_BYTE_LOG2   3
#define PR_BITS_PER_SHORT_LOG2  4
#define PR_BITS_PER_INT_LOG2    5
#define PR_BITS_PER_INT64_LOG2  6
#if defined(RT_ARCH_AMD64) || defined(RT_ARCH_ARM64)
# define PR_BITS_PER_LONG_LOG2   6
#else
# define PR_BITS_PER_LONG_LOG2   5
#endif
#define PR_BITS_PER_FLOAT_LOG2  5

#ifndef XP_UNIX
# define XP_UNIX
#endif

#ifdef RT_OS_DARWIN
# define DARWIN
#elif defined(RT_OS_FREEBSD)
# define FREEBSD
#elif defined(RT_OS_LINUX)
# define LINUX
#elif defined(RT_OS_NETBSD)
# define NETBSD
#elif defined(RT_OS_OPENBSD)
# define OPENBSD
#elif defined(RT_OS_SOLARIS)
# define SOLARIS
#else
# error "Define the correct platform identifier / Port me."
#endif

#endif /* !nspr_vboxcfg___ */
