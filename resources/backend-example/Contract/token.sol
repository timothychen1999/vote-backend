// SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;

import "@openzeppelin/contracts@4.9.0/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts@4.9.0/security/Pausable.sol";
import "@openzeppelin/contracts@4.9.0/access/AccessControl.sol";
import "@openzeppelin/contracts@4.9.0/token/ERC20/extensions/draft-ERC20Permit.sol";

/// @custom:security-contact r10922188@csie.ntu.edu.tw
contract PawPrint is ERC20, Pausable, AccessControl, ERC20Permit {
    bytes32 public constant PAUSER_ROLE = keccak256("PAUSER_ROLE");
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    uint256 priceRatio = 1000000000000000;
    constructor() ERC20("PawPrint", "PP") ERC20Permit("PawPrint") {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(PAUSER_ROLE, msg.sender);
        _mint(msg.sender, 10000 * 10 ** decimals());
        _grantRole(MINTER_ROLE, msg.sender);
    }
    event RatioSet(uint256 newRatio);
    function  setPriceRatio(uint256 ratio) public {
        priceRatio = ratio;
        emit RatioSet(ratio);
    }
    

    function pause() public onlyRole(PAUSER_ROLE) {
        _pause();
    }

    function unpause() public onlyRole(PAUSER_ROLE) {
        _unpause();
    }

    function mint(address to, uint256 amount) public onlyRole(MINTER_ROLE) {
        _mint(to, amount);
    }
    function buyToken(uint256 amount) public  payable whenNotPaused {
        require(amount > 0, "Can not buy zero");
        require(amount*priceRatio == msg.value,"Wrong Pricing");
        _mint(msg.sender,amount);
    }
    function checkBalance() public view returns(uint256){
        return address(this).balance;
    }
    function retriveBalance(uint256 amount)public onlyRole(DEFAULT_ADMIN_ROLE){
        payable(msg.sender).transfer(amount);
    }
    function _beforeTokenTransfer(address from, address to, uint256 amount)
        internal
        whenNotPaused
        override
    {
        super._beforeTokenTransfer(from, to, amount);
    }
}
