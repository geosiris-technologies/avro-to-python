// SPDX-FileCopyrightText: 2023 Geosiris
// SPDX-License-Identifier: Apache-2.0 OR MIT
use etptypes::message::*;

#[test]
fn test_message_flags_0() {
	let full_0 : MessageHeaderFlag = MessageHeaderFlag{
		msg_final:  false,
		msg_compressed: false,
		msg_aknowledge: false,
		msg_has_header_extension: false,
	};

	assert_eq!(full_0, full_0);

	let int_rep : i32 = full_0.as_i32();

	assert_eq!(int_rep, 0);
}

#[test]
fn test_message_flags_0_parse() {
	let full_0 : MessageHeaderFlag = MessageHeaderFlag{
		msg_final:  false,
		msg_compressed: false,
		msg_aknowledge: false,
		msg_has_header_extension: false,
	};
	assert_eq!(full_0, MessageHeaderFlag::parse(full_0.as_i32()));
}

#[test]
fn test_message_flags_1() {
	let full_1 : MessageHeaderFlag = MessageHeaderFlag{
		msg_final:  true,
		msg_compressed: true,
		msg_aknowledge: true,
		msg_has_header_extension: true,
	};

	assert_eq!(full_1, full_1);

	let int_rep : i32 = full_1.as_i32();

	assert_eq!(int_rep, MSG_FLAG_FINAL | MSG_FLAG_COMPRESSED | MSG_FLAG_ACKNOWLEDGE | MSG_FLAG_HEADER_EXTENSION);
}

#[test]
fn test_message_flags_1_parse() {
	let full_1 : MessageHeaderFlag = MessageHeaderFlag{
		msg_final:  true,
		msg_compressed: true,
		msg_aknowledge: true,
		msg_has_header_extension: true,
	};
	assert_eq!(full_1, MessageHeaderFlag::parse(full_1.as_i32()));
}

#[test]
fn test_message_flags_mix_as_int32() {
	let full_1 : MessageHeaderFlag = MessageHeaderFlag{
		msg_final:  true,
		msg_compressed: false,
		msg_aknowledge: true,
		msg_has_header_extension: false,
	};
	let int_rep = full_1.as_i32();

	assert_eq!((int_rep & MSG_FLAG_FINAL), MSG_FLAG_FINAL);
	assert_eq!((int_rep & MSG_FLAG_COMPRESSED), 0);
	assert_eq!((int_rep & MSG_FLAG_ACKNOWLEDGE), MSG_FLAG_ACKNOWLEDGE);
	assert_eq!((int_rep & MSG_FLAG_HEADER_EXTENSION), 0);
}

#[test]
fn test_message_flags_mix_parse() {
	let full_1 : MessageHeaderFlag = MessageHeaderFlag{
		msg_final:  true,
		msg_compressed: false,
		msg_aknowledge: true,
		msg_has_header_extension: false,
	};
	let int_rep = full_1.as_i32();
	let full_1_parsed : MessageHeaderFlag = MessageHeaderFlag::parse(int_rep);

	assert_eq!(full_1_parsed.msg_final, true);
	assert_eq!(full_1_parsed.msg_compressed, false);
	assert_eq!(full_1_parsed.msg_aknowledge, true);
	assert_eq!(full_1_parsed.msg_has_header_extension, false);
}