// SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;

import "@openzeppelin/contracts@4.9.0/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts@4.9.0/token/ERC721/extensions/ERC721Burnable.sol";
import "@openzeppelin/contracts@4.9.0/access/AccessControl.sol";
import "@openzeppelin/contracts@4.9.0/utils/Counters.sol";

/// @custom:security-contact r10922188@csie.ntu.edu.tw
contract CatToken is ERC721, ERC721Burnable, AccessControl {
    using Counters for Counters.Counter;
    mapping (address => bool) Claimed;
    mapping (uint256 => bool) AllowTransfer;
    function hasClaimed(address addr) public view returns (bool){
        return Claimed[addr];
    }
    function contractURI() public pure returns (string memory) {
        return "https://pawtopia.ddns.net/api/metadata/contract-cat";
    }
    function isAllowTransfer(uint256 tid) public  view returns (bool){
        return AllowTransfer[tid];
    }
    function setAllowTransfer(uint256 tid,bool alo) public  onlyRole(DEFAULT_ADMIN_ROLE){
        AllowTransfer[tid] = alo;
    }

    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    Counters.Counter private _tokenIdCounter;

    constructor() ERC721("CatToken", "PAW") {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(MINTER_ROLE, msg.sender);
    }

    function _baseURI() internal pure override returns (string memory) {
        return "https://pawtopia.ddns.net/api/metadata/";
    }
    function claim() public {
        require(Claimed[msg.sender]==false,"Already Claimed");
        Claimed[msg.sender] = true;
        uint256 tokenId = _tokenIdCounter.current();
        _tokenIdCounter.increment();
        _safeMint(msg.sender, tokenId);
    }
    

    function safeMint(address to) public onlyRole(MINTER_ROLE) {
        uint256 tokenId = _tokenIdCounter.current();
        _tokenIdCounter.increment();
        _safeMint(to, tokenId);
    }

    // The following functions are overrides required by Solidity.

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, AccessControl)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
    function _beforeTokenTransfer(address from, address to, uint256 tid,uint256 batch)
        internal virtual override // Add virtual here!
    {
        super._beforeTokenTransfer(from, to, tid, batch); // Call parent hook
        require(batch==1,"No Batch opperation is allowed!");
        require(from==address(0)||to==address(0)||AllowTransfer[tid],"Don't transfer your pet, permission from admin is needed");

    }
}
