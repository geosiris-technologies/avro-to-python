#![allow(unused_imports)]
#![allow(dead_code)]

use crate::energistics::etp::v12::datatypes::message_header_extension::MessageHeaderExtension;
use crate::energistics::etp::v12::datatypes::message_header::MessageHeader;

#[derive(Debug, PartialEq, Clone, serde::Deserialize, serde::Serialize)]
pub struct Message<T>{
	header: MessageHeader,
	header_extension: Option<MessageHeaderExtension>,
	body: T,
}

pub const MSG_FLAG_FINAL: i32 = 0x02;
pub const MSG_FLAG_COMPRESSED: i32 = 0x08;
pub const MSG_FLAG_ACKNOWLEDGE: i32 = 0x10;
pub const MSG_FLAG_HEADER_EXTENSION: i32 = 0x20;

#[derive(Debug, PartialEq, Clone, serde::Deserialize, serde::Serialize)]
pub struct MessageHeaderFlag{
	pub msg_final: bool,
	pub msg_compressed: bool,
	pub msg_aknowledge: bool,
	pub msg_has_header_extension: bool,
}

impl MessageHeaderFlag {
	pub fn as_i32(&self) -> i32 {
		(if self.msg_final {MSG_FLAG_FINAL} else {0})
		| (if self.msg_compressed {MSG_FLAG_COMPRESSED} else {0})
		| (if self.msg_aknowledge {MSG_FLAG_ACKNOWLEDGE} else {0})
		| (if self.msg_has_header_extension {MSG_FLAG_HEADER_EXTENSION} else {0})
	}

	pub fn parse(flag: i32) -> MessageHeaderFlag {
		MessageHeaderFlag{
			msg_final: (flag & MSG_FLAG_FINAL) != 0,
			msg_compressed: (flag & MSG_FLAG_COMPRESSED) != 0,
			msg_aknowledge: (flag & MSG_FLAG_ACKNOWLEDGE) != 0,
			msg_has_header_extension: (flag & MSG_FLAG_HEADER_EXTENSION) != 0,
		}
	}
}